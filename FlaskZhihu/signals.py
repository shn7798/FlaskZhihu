from blinker import Namespace

signals = Namespace()
#
# signals_names = [
#     'question_answer_add',
#     'question_follow',
#     'question_unfollow',
#     'question_comment_add',
#     'question_comment_delete',
#     'answer_comment_add',
#     'answer_comment_delete',
#     'answer_voteup',
#     'answer_votedown',
#     'answer_cancel_vote',
# ]
#
# signals_defines = dict()
# for name in signals_names:
#     print "%s = signals.signal('%s')" % (name, name)
#     signals_defines[name] = signals.signal(name)
#
# globals().update(signals_defines)
#
# __all__ = signals_names

question_answer_add = signals.signal('question_answer_add')
question_follow = signals.signal('question_follow')
question_unfollow = signals.signal('question_unfollow')
question_comment_add = signals.signal('question_comment_add')
question_comment_delete = signals.signal('question_comment_delete')
answer_comment_add = signals.signal('answer_comment_add')
answer_comment_delete = signals.signal('answer_comment_delete')
answer_voteup = signals.signal('answer_voteup')
answer_votedown = signals.signal('answer_votedown')
answer_cancel_vote = signals.signal('answer_cancel_vote')
comment_voteup = signals.signal('comment_voteup')
comment_cancel_vote = signals.signal('comment_cancel_vote')
collection_answer_add = signals.signal('collection_answer_add')
collection_answer_delete = signals.signal('collection_answer_delete')
collection_follow = signals.signal('collection_follow')
collection_unfollow = signals.signal('collection_unfollow')