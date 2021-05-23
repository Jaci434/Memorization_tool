import random
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# create the connection
engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

# meta hold collection of table objects + optional binding to engine or connetion
"""meta = MetaData()

flashcards_table = Table(
    'flashcards', meta,
    Column('id',Integer, primary_key=True),
    Column('first_column',String),
    Column('second_column', String),
)

meta.create_all(engine)
"""
# base class= sotres catalog of classes and mappes tables
Base = declarative_base()


# class to store answers and questions in database
class flashcards_table(Base):
    __tablename__ = 'flashcards_table'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)


# create the corresponding table in the database
Base.metadata.create_all(engine)

# creating a handle - make an object od session class and use it as handle
# ti interact with database
Session = sessionmaker(bind=engine)
session = Session()


class flashcards():

    def __init__(self):
        self.question = None
        self.answer = None

    def add_new_flashcard(self):
        self.question = input('Question:\n')
        while (self.question == ""):
            self.question = input('Question:\n')
        self.answer = input('Answer:\n')
        while (self.answer == ""):
            self.answer = input('Answer:\n')
        # flashcards.flashcards[self.question] = self.anwser
        # using databse
        new_data = flashcards_table(first_column=self.question, second_column=self.answer)
        session.add(new_data)
        session.commit()
        id_all_new = session.query(flashcards_table.id).count()
        return id_all_new

    def Leitner_system(self, checking_input, index, box1, box2, box3):

        if checking_input == "y":
            if index in box1:
                box2.append(index)
                box1.remove(index)
            elif index in box2:
                box3.append(index)
                box2.remove(index)
            elif index in box3:
                box3.remove(index)
                del_data = session.query(flashcards_table).all()[0]
                session.delete(del_data)
                session.commit()
        elif checking_input == "n":
            if index in box3:
                box1.append(index)
                box3.remove(index)
            elif index in box2:
                box1.append(index)
                box2.remove(index)
        else:
            print(f'{checking_input} is not an option')
        return box1, box2, box3

    def practice_flashcards(self, box1, box2, box3):

        if id_all == 0:
            print('There is no flashcard to practice!')
        else:
            question_index = 0
            flashcard = session.query(flashcards_table).all()
            while (True):

                if len(box1) == 0 and len(box2) == 0 and len(box3) == 0:
                    print('There is no flashcard to practice!')
                    break

                if question_index == id_all:
                    question_index = 0

                self.question = flashcard[question_index].first_column
                self.answer = flashcard[question_index].second_column
                print(f'Question:{self.question}')
                print('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:')
                input_y_n_u = input()

                if input_y_n_u == 'y':
                    print(f'Answer:{self.answer}')
                    print('press "y" if your answer is correct:\npress "n" if your answer is wrong:')
                    checking_input = input()
                    box1, box2, box3 = flashcards.Leitner_system(self, checking_input, question_index, box1, box2, box3)
                    question_index += 1

                elif input_y_n_u == 'n':
                    print('press "y" if your answer is correct:\npress "n" if your answer is wrong:')
                    checking_input = input()
                    box1, box2, box3 = flashcards.Leitner_system(self, checking_input, question_index, box1, box2, box3)
                    question_index += 1
                    continue
                elif input_y_n_u == 'u':
                    print('press "d" to delete the flashcard:\npress "e" to edit the flashcard:')
                    input_d_e = input()
                    current_card = flashcard[question_index]

                    if input_d_e == 'd':
                        session.delete(current_card)
                        session.commit()
                        question_index += 1

                    elif input_d_e == 'e':
                        print(f'current question: {self.question}')
                        change_question = input('please write a new question:')
                        print(f'current answer: {self.answer}')
                        change_answer = input('please write a new answer:')

                        if change_question == '' and change_answer == '':
                            question_index += 1
                            continue
                        elif change_answer == '':
                            current_card.first_column = change_question
                            session.commit()
                            question_index += 1
                        elif change_question == '':
                            current_card.second_column = change_answer
                            session.commit()
                            question_index += 1
                        else:
                            current_card.first_column = change_question
                            current_card.second_column = change_answer
                            session.commit()
                            question_index += 1
                    else:
                        print(f'{input_d_e} is not an option')

                else:
                    print(f'{input_y_n_u} is not an option')


id_all = session.query(flashcards_table.id).count()
box1 = [x for x in range(id_all)]
box2 = []
box3 = []

while (True):

    print('1. Add flashcards\n2. Practice flashcards\n3. Exit')
    try:
        user_input = input()
        cards = flashcards()

        user_input_1 = int(user_input)

        if user_input_1 == 1:
            while (True):
                print('1. Add a new flashcard\n2. Exit')
                try:
                    user_input_2 = input()
                    user_input_2_int = int(user_input_2)
                    if user_input_2_int == 1:
                        new_id_all = cards.add_new_flashcard()
                        if new_id_all != id_all:
                            id_all = new_id_all
                            box1 = [x for x in range(id_all)]
                        continue
                    if user_input_2_int == 2:
                        break
                    else:
                        print(f'{user_input_2_int} is not an option')
                except ValueError:
                    print(f'{user_input_2} is not an option')

        elif user_input_1 == 2:
            cards.practice_flashcards(box1, box2, box3)

        elif user_input_1 == 3:
            print('Bye!')
            exit()
        else:
            print(f'{user_input_1} is not an option')
    except ValueError:
        print(f'{user_input} is not an option')
