from sqlalchemy import Column, LargeBinary, Numeric, UnicodeText

from julia.modules.sql import BASE, SESSION


class NOTES(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    note = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    note_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(
        self,
        chat_id,
        keyword,
    ):
        self.chat_id = chat_id
        self.keyword = keyword

NOTES.__table__.create(checkfirst=True)


def get_notes(chat_id, keyword):
    try:
        return SESSION.query(NOTES).get((str(chat_id), keyword))
    except:
        return None
    finally:
        SESSION.close()


def get_all_notes():
    try:
        SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id)).all()
    except:
        return None
    finally:
        SESSION.close()


def add_note(chat_id, keyword):
    adder = SESSION.query(NOTES).get(chat_id, keyword)
    if adder:
        adder.keyword = keyword
    else:
        adder = NOTES(chat_id, keyword)
    SESSION.add(adder)
    SESSION.commit()


def remove_note(chat_id, keyword):
    saved_note = SESSION.query(NOTES).get((str(chat_id), keyword))
    if saved_note:
        SESSION.delete(saved_note)
        SESSION.commit()

def remove_all_notes(chat_id):
    saved_note = SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id))
    if saved_note:
        saved_note.delete()
        SESSION.commit()
