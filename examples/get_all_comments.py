"""Example of getting all comments from a video."""

from __future__ import annotations

import time
from datetime import datetime

from niconico import NicoNico
from niconico.exceptions import CommentAPIError

FAILED_TRY_COUNT = 5

niconico_client = NicoNico()
niconico_client.login_with_mail("sample@example.com", "password")

video_id = "sm43236191"
watch_data = niconico_client.video.watch.get_watch_data(video_id)

when_unix = int(time.time())
main_min_no = 0
owner_comments_fecthed = False
is_finished = False
comment_count = 0
failed_count = 0
thread_key = None

comments_dict: dict[str, list] = {"main": [], "owner": [], "easy": []}


while not is_finished:
    try:
        comment_res = niconico_client.video.watch.get_comments(watch_data, when=when_unix, thread_key=thread_key)
    except CommentAPIError as e:
        if e.message == "EXPIRED_TOKEN":
            thread_key = niconico_client.video.watch.get_thread_key(video_id)
            time.sleep(1)
            continue
    if comment_res is None:
        if failed_count >= FAILED_TRY_COUNT:
            break
        failed_count += 1
        time.sleep(60)
        continue
    for thread in comment_res.threads:
        if thread.fork == "owner":
            if owner_comments_fecthed:
                continue
            owner_comments_fecthed = True
            comment_count += len(thread.comments)
            thread.comments.reverse()
            comments_dict[thread.fork].extend(thread.comments)
        elif thread.fork == "easy":
            if len(thread.comments) <= 0:
                continue
            comment_count += len(thread.comments)
            thread.comments.reverse()
            comments_dict[thread.fork].extend(thread.comments)
        else:
            if main_min_no == 0:
                main_min_no = thread.comments[-1].no + 1
            comment_index = len(thread.comments) - 1
            while comment_index >= 0:
                if thread.comments[comment_index].no < main_min_no:
                    break
                comment_index -= 1
            comments = thread.comments[: comment_index + 1]
            if len(comments) <= 0:
                is_finished = True
                continue
            comment_count += len(comments)
            main_min_no = thread.comments[0].no
            when_unix = int(datetime.fromisoformat(thread.comments[0].posted_at).timestamp())
            comments.reverse()
            comments_dict[thread.fork].extend(comments)
    print(f"Comment Updated: {comment_count}")
    time.sleep(1)

print(f"Total comments: {comment_count}")
print(f"Main comments: {len(comments_dict['main'])}")
print(f"Owner comments: {len(comments_dict['owner'])}")
print(f"Easy comments: {len(comments_dict['easy'])}")
print(comments_dict["main"][0])
print(comments_dict["easy"][0])
