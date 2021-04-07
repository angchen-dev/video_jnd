from videoJnd.models import EtJndParticipant, EtJndHit, EtJndResult
import uuid
import random
from datetime import datetime

def select_hits(recv_data:dict) -> dict:
    try:
        worker_id = recv_data['worker_id']
        if not worker_id:
            left_hits = ["HIT1", "HIT2", "HIT3", "HIT4", "HIT5"]
            random.shuffle(left_hits)
            cur_hit = left_hits.pop()
            wuid = uuid.uuid4() 
            EtJndParticipant(wuid = wuid,
                            left_hits = {"hits":left_hits},
                            cur_hit = cur_hit).save()
            
            cur_hit_obj = EtJndHit.objects.filter(name=cur_hit)[0]

            return {"status":"successful", "data":{"wuid": wuid, 
                                                    "hit_id": cur_hit_obj.huid,
                                                    "image_url": cur_hit_obj.image_url, 
                                                    "image_gts": cur_hit_obj.image_gts, 
                                                    "test_gt": cur_hit_obj.test_gt}}
        else:
            cur_p = EtJndParticipant.objects.filter(wuid=worker_id)[0]
            if cur_p.finish_all_hits:
                return {"status":"failed", "data":"You finished all HITs, Thank you very much."}
            else:
                cur_hit_obj = EtJndHit.objects.filter(name=cur_p.cur_hit)[0]

                return {"status":"successful", "data":{"hit_id": cur_hit_obj.huid,
                                                        "image_url": cur_hit_obj.image_url, 
                                                        "image_gts": cur_hit_obj.image_gts, 
                                                        "test_gt": cur_hit_obj.test_gt}}

    except Exception as e:
        print("select_hits error: %s" % str(e))
        return {"status":"failed", "data":"system error"}

def record_result(recv_data:dict) -> dict:
    try:
        EtJndResult(hit_id = recv_data["hit_id"],
                worker_id = recv_data["worker_id"],
                result = recv_data["result"],
                accept_time = recv_data["accept_time"]).save()

        cur_p = EtJndParticipant.objects.filter(wuid=recv_data["worker_id"])[0]

        cur_p.cur_hit = ""
        
        left_hits = cur_p.left_hits["hits"]
        if len(left_hits) == 0 :
            cur_p.finish_all_hits = True
        else:
            random.shuffle(left_hits)
            cur_hit = left_hits.pop()
            cur_p.cur_hit = cur_hit
            cur_p.left_hits = {"hits":left_hits}
        cur_p.save()

        cur_hit_obj = EtJndHit.objects.filter(huid=recv_data["hit_id"])[0]
        cur_hit_obj.count = cur_hit_obj.count + 1
        cur_hit_obj.save()
        
        return {"status":"successful"}
    except Exception as e:
        print("select_hits error: %s" % str(e))
        return {"status":"failed", "data":"system error"} 