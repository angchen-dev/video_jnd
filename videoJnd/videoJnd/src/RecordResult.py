from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import VideoObj, Experiment, Participant, RatingHistory
from videoJnd.src.GetConfig import get_config


import random
import uuid
import copy
import ast

config = get_config()
QP_TRIAL_NUM = config["QP_TRIAL_NUM"]

def record_result(recv_data:dict) -> dict:
    p_obj = Participant.objects.filter(puid=recv_data["puid"])
    if p_obj:
        p_obj = p_obj[0]
        result = recv_data["result"]

        for video_result in result:
            video_obj = VideoObj.objects.filter(vuid=video_result["vuid"])

            if video_obj:
                video_obj = video_obj[0]
                if video_obj.ongoing:
                    _update_video_db(video_result, video_obj)
                    # TODO: add history, for each request or each video?
                    # TODO: participant DB, change to task DB, 
                    # TODO: record gt-side, reported side

                else:
                    return {"status":"failed", 
                            "restype": "record_result",
                            "data":"video %s is not ongoing" % video_result["vuid"]}
            else:
                return {"status":"failed", 
                        "restype": "record_result",
                        "data":"video %s is not exist" % video_result["vuid"]}

        _set_p_onging_false(p_obj)

        return {"status":"successful", "restype": "record_result",}
    else:
        return {"status":"failed", "restype": "record_result", "data":"participant is not exist"}

def _update_video_db(video_result:dict, video_obj:object) -> None:
    decision_code = _encode_decision(video_result["side"], video_result["decision"])
    video_obj.result_orig = _add_new_item(video_obj.result_orig, 
                                            decision_code + "-" + video_result["side"] + "-" + video_result["decision"])

    video_obj.result_code = _add_new_item(video_obj.result_code, decision_code)
    video_obj.qp = _add_new_item(video_obj.qp, video_result["qp"])
    video_obj.ongoing = False
    
    # TODO: don't update qp_count when the result code is 4
    video_obj.qp_count = video_obj.qp_count + 1 
    if video_obj.qp_count == QP_TRIAL_NUM:
        video_obj.is_finished = True
    
    video_obj.cur_participant = None
    video_obj.cur_participant_uid = None
    video_obj.participant_start_date = None

    video_obj.save()

def _set_p_onging_false(p_obj: object) -> None:
    p_obj.ongoing= False
    p_obj.save()

def _encode_decision(side:str, decision:str) -> str:
    if decision == "R" or decision == "L":
        if decision == side:
            return "1"
        elif decision != side:
            return "2"
    elif decision == "not sure":
        return "3"
    elif decision == "no decision":
        return "4"

def _add_new_item(crr_str:str, new_item:str) -> str:
    if crr_str:
        crr_str += ","+new_item
    else:
        crr_str = new_item
    
    return crr_str

