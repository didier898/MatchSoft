from django.core.management.base import BaseCommand
from core.models import Question, Choice
import random

DATA_OK = [
    (1,  "Resuelve: x + 3 = 8",                       "5",   ["-5","11","8"],                "x = 8 - 3 = 5"),
    (2,  "Resuelve: x - 7 = 2",                       "9",   ["-5","5","-9"],               "x = 2 + 7 = 9"),
    (3,  "Resuelve: 3x = 12",                         "4",   ["36","-4","12"],              "x = 12/3 = 4"),
    (4,  "Resuelve: 5x = -20",                        "-4",  ["4","-25","20"],              "x = -20/5 = -4"),
    (5,  "Resuelve: 2x + 4 = 10",                     "3",   ["-3","6","-2"],               "2x = 6 → x = 3"),
    (6,  "Resuelve: 4x - 6 = 2",                      "2",   ["-2","-1","8"],               "4x = 8 → x = 2"),
    (7,  "Resuelve: (x/3) + 2 = 5",                   "9",   ["1","-9","6"],                "x/3 = 3 → x = 9"),
    (8,  "Resuelve: (x - 2)/4 = 3",                   "14",  ["10","-14","4"],              "x - 2 = 12 → x = 14"),
    (9,  "Resuelve: 2(x + 1) = 10",                   "4",   ["5","6","-4"],                "2x + 2 = 10 → x = 4"),
    (10, "Resuelve: 3(x - 2) = 9",                    "5",   ["3","-5","7"],                "3x - 6 = 9 → x = 5"),
    (11, "Resuelve: 7x + 5 = 2x + 30",                "5",   ["-5","25","-25"],             "5x = 25 → x = 5"),
    (12, "Resuelve: 6x - 8 = 2x + 12",                "5",   ["-5","4","-4"],               "4x = 20 → x = 5"),
    (13, "Resuelve: (x/2) - 3 = 4",                   "14",  ["7","-14","-7"],              "x/2 = 7 → x = 14"),
    (14, "Resuelve: 5(x + 1) - 2x = 14",              "3",   ["4","5","-3"],                "5x+5 -2x = 14 → 3x = 9 → x = 3"),
    (15, "Resuelve: 2(3x - 1) = x + 8",               "2",   ["3","4","5"],                 "6x - 2 = x + 8 → 5x = 10 → x = 2"),
    (16, "Resuelve: (x - 1)/5 + (x + 2)/10 = 3",      "10",  ["7","5","8"],                 "mcm=10 → 2(x-1)+(x+2)=30 → 3x=30 → x=10"),
    (17, "Resuelve: (2x - 3)/5 = (x + 2)/5",          "5",   ["3","7","9"],                 "2x - 3 = x + 2 → x = 5"),
    (18, "Resuelve: 5 - (2x - 1) = 3x + 4",           "0.4", ["-0.4","2","-2"],             "6 - 2x = 3x + 4 → -5x = -2 → x = 0.4"),
    (19, "Resuelve: 3(x - 2) + 4(x + 1) = 5x + 10",   "6",   ["4","5","8"],                 "7x - 2 = 5x + 10 → 2x = 12 → x = 6"),
    (20, "Resuelve: (x + 3)/2 - (x - 1)/3 = 5",       "19",  ["17","16","14"],              "mcm=6 → 3(x+3) - 2(x-1) = 30 → x+11=30 → x=19"),
]

class Command(BaseCommand):
    help = "Carga 20 preguntas de ecuaciones lineales (1 incógnita) en 'core'"

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        created = 0
        for diff, text, correct, wrongs, expl in DATA_OK:
            q = Question.objects.create(text=text, difficulty=diff, explanation=expl)
            options = [correct] + wrongs
            random.shuffle(options)
            labels = ['A','B','C','D']
            for i, opt in enumerate(options[:4]):
                Choice.objects.create(
                    question=q,
                    label=labels[i],
                    text=str(opt),
                    is_correct=(opt == correct)
                )
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Preguntas creadas: {created}'))
