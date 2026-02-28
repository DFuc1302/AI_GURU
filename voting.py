# core/voting.py

def voting_engine(r1, r2):

    if not r1 or not r2:
        return None, False

    f1 = r1.get("formula")
    f2 = r2.get("formula")

    if f1 == f2:
        return r1, True

    # nếu khác, ưu tiên cái không None
    if f1 and not f2:
        return r1, False
    if f2 and not f1:
        return r2, False

    return r1, False