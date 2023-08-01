from rest_framework.views import APIView
from django.http import HttpResponse
from datetime import datetime
import json
import pytz

from posts.models import dbposts, dbquestions, dbreplies

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

class POSTS(APIView):
    def get(self, rquest):
        post_list = dbposts.objects.all()
        question_list = dbquestions.objects.all()
        reply_list = dbreplies.objects.all()

        params = {
            "post_list": []
        }

        for p in post_list:
            post_info = {
                "post_id": p.id,
                "user_id": p.user_id,
                "user_name": p.user_name,
                "post_text": p.text,
                "category": p.category,
                "comment_cnt": p.comment_cnt,
                "created_at": p.created_at,
            }
            params["post_list"].append(post_info)

        params["post_list"] = sorted(params["post_list"], key=lambda x:x["created_at"], reverse=True)

        question_dict = {}
        for q in question_list:
            question_info = {
                "question_id": q.id,
                "post_id": q.post_id,
                "text": q.text,
                "created_at": q.created_at
            }
            post_id = q.post_id
            if post_id not in question_list:
                question_dict[post_id] = [question_info]
            else:
                question_dict[post_id].append(question_info)

        reply_dict = {}
        for r in reply_list:
            reply_info = {
                "reply_id": r.id,
                "question_id": r.question_id,
                "text": r.text,
                "created_at": r.created_at
            }
            question_id = r.question_id
            if question_id not in reply_dict.keys():
                reply_dict[question_id] = [reply_info]
            else:
                reply_dict[question_id].append(reply_info)

        for i in range(len(params["post_list"])):
            if params["post_list"][i]["post_id"] not in question_dict.keys():
                continue
            post_id = params["post_list"][i]["post_id"]
            q_list = question_dict[post_id]
            q_list = sorted(q_list, key=lambda x:x["created_at"])
            params["post_list"][i]["question_list"] = q_list

            for j in range(len(q_list)):
                if q_list[j]["question_id"] not in reply_dict.keys():
                    continue
                question_id = q_list[j]["question_id"]
                r_list = reply_dict[question_id]
                r_list = sorted(r_list, key=lambda x:x["created_at"])
                params["post_list"][i]["question_list"][j]["reply_list"] = r_list

        print(f"最終結果:{params}")

        json_str = json.dumps(params, default=json_serial) 
        return HttpResponse(json_str)

    def post(self, request):
        dbposts.objects.create(user_id="hogehoge", user_name="watashi", text="今日も楽しかった", 
                               category="restaurant", comment_cnt=0, 
                               created_at=datetime.now(pytz.timezone('Asia/Tokyo')))
        return HttpResponse("got it!!")


class QUESTIONS(APIView):
    def get(self, request, post_id):
        question_list = dbquestions.objects.all()
        for q in question_list:
            print(f"id:{q.id}, post_id:{q.post_id}, text:{q.text}, crested_at:{q.created_at}")

        return HttpResponse("got it!!!")

    def post(self, request, post_id):
        print(post_id)
        body = json.loads(request.body)
        question_text = body["text"]
        print(question_text)

        dbquestions.objects.create(post_id=post_id, text=question_text, 
                                   created_at=datetime.now(pytz.timezone('Asia/Tokyo')))
        return HttpResponse("got it!!!")

class REPLIES(APIView):
    def get(self, request, post_id, question_id):
        relies_list = dbreplies.objects.all()
        for r in relies_list:
            print(f"id:{r.id}, question_id:{r.question_id}, text:{r.text}, created_at:{r.created_at}")

        return HttpResponse("got it!!!")

    def post(self, request, post_id, question_id):
        print(question_id)
        body = json.loads(request.body)
        reply_text = body["text"]
        print(reply_text)

        dbreplies.objects.create(question_id=question_id, text=reply_text,
                                 created_at=datetime.now(pytz.timezone('Asia/Tokyo')))
        
        return HttpResponse("got it!!!!!")
        
