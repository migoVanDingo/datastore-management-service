import random
import string
import traceback
from flask import Blueprint, current_app, json
import time

from utility.constant import Constant
from utility.payload.request_payload import RequestPayload
from utility.request import Request


utility_api = Blueprint('utility_api', __name__)

@utility_api.route('/utility/datastore/add-aolme-videos', methods=['GET'])
def health():
    try:
        dao_request = Request()
        add_videos_response = dao_request.read_all(request_id="READ_ALL", query="SELECT * FROM aolme_videos WHERE set_id IS NULL AND idx BETWEEN 6001 AND 7000")
        #8786
        current_app.logger.info(f"Response len: {len(add_videos_response['response'])}")

        if not add_videos_response["response"]:
            raise Exception(f"Failed to get videos list")

        # Videos list are rows where set_id is null
        videos = [video for video in add_videos_response["response"] if video["set_id"] is None or video["set_id"] == ""]

        current_app.logger.info(f"Videos len: {len(videos)}")

        group_dict = {}

        count = 1
        # For each video,
        for video in videos:

            new_request = Request()
            if count % 100 == 0:
                print("Sleeping for 10 second...")
                time.sleep(1)
                

            if video['set_id'] is not None:
                print(f"SET_ID IS NOT NONE -- Skipping video: {video['video_name']}")
                continue

            # Parse the video name
            video_name = video["video_name"]

            # Split by _ and get first element. 
            name_split = video_name.split("_")

            # If element not in dictionary add it as key and generate q2 and q3 subfields.
            current_set_id = "" 
            
            new_index = name_split[0] + "_" + name_split[1]
            if len(name_split) >= 2:
                
                if new_index not in group_dict:
                    # Check if second element is q2 or q3, if value is null generate set_id and update the video record with the set_id
                    current_set_id = generate_id()
                    if name_split[1] == "q2":
                        group_dict[new_index] = {"q2": current_set_id, "q3": None}
                    elif name_split[1] == "q3":
                        group_dict[new_index] = {"q2": None, "q3": current_set_id}
                else:
                    # Else get the set_id and update the video record with the set_id
                    current_set_id = group_dict[new_index]["q2"] if name_split[1] == "q2" else group_dict[new_index]["q3"]
            else: 
                print(f"NAME_SPLIT_WEIRD -- Skipping video: {video_name}")
                continue

            
            
            # Update set_name with first element
            new_request.update("UPDATE_AOLME_VIDEOS", "aolme_videos", "video_id", video["video_id"], {"set_id": current_set_id, "set_name": new_index})

            # Then create a files record payload
            # {datastore_id, file_path="metadata", file_name, file_type="video", file_size="null", create_method="LINK", created_by="DEVROOT", metadata={video_id="video_id from video table", set_id="set_id from video table", url="link from video table", cohort, level, school, quality, date, facilitator, group_name} }

            current_in_set = None
            total_in_set = None
            if len(name_split) > 2 and "-" in name_split[2]:
                set_num_split = name_split[2].split("-")
            

                total_in_set = set_num_split[1].replace(".mp4", "")
                current_in_set = set_num_split[0]
                #remove leading zero from current_in_set
                current_in_set = current_in_set.lstrip("0")


            metadata = {
                "video_id": video["video_id"],
                "set_id": current_set_id,
                "set_name": new_index,
                "url": video["link"],
                "cohort": video["cohort"],
                "level": video["level"],
                "school": video["school"],
                "quality": video["quality"],
                "date": video["date"],
                "facilitator": video["facilitator"],
                "group_name": video["group_name"],
                "video_name": video_name,
                "index_in_set": current_in_set,
                "total_in_set": total_in_set
            }

            data = {
                "datastore_id": "DST872RMUXRDUUYRBO3TKZIS0",
                "file_path": "metadata",
                "file_name": video_name,
                "file_type": "video",
                "create_method": "LINK",
                "created_by": "DEVROOT",
                "metadata": json.dumps(metadata)

            }
            
            insert_response = new_request.insert("INSERT_AOLME_FILES", Constant.table["FILES"], data)
            if not insert_response["response"]:
                raise Exception(f"Failed to insert record for video: {video_name}")

            count += 1
            print(f"Added video: {video['idx']}. {video_name}")

            # Insert record into files table
        return {"message": f"\n\nSuccessfully added videos", "status": 200}

    except Exception as e:
        return f"An Error Occurred: {traceback.format_exc()} -- {e}"

def generate_id() -> str:
        prefix = "VDST"
        N = 25
        id = prefix + ''.join(random.choices(string.digits, k= N - len(prefix) - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        return id