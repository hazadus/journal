import os
from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

import xlsxwriter

from journal.models import Task

REPORT_DIR = os.path.join(settings.MEDIA_ROOT, "reports")


class Command(BaseCommand):
    help = "Создаёт отчет по текущим задачам в формате Excel."

    def handle(self, *args, **options):
        filename = "Report_" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".xlsx"
        report_path = os.path.join(REPORT_DIR, filename)

        if not os.path.exists(REPORT_DIR):
            os.mkdir(REPORT_DIR)

        tasks = Task.objects.filter(is_private=False, is_completed=False, is_archived=False)

        workbook = xlsxwriter.Workbook(report_path)
        bold = workbook.add_format({"bold": True})
        date_format = workbook.add_format({"num_format": "dd.mm.yyyy hh:mm"})

        for i, task in enumerate(tasks):
            print(task)
            worksheet = workbook.add_worksheet(name="{num}. {title}".format(
                num=i + 1,
                title=task.title[:26]  # max len = 31
            ))

            worksheet.set_column(0, 0, 100)
            worksheet.set_column(1, 2, 15)

            worksheet.write(0, 0, task.title, bold)
            worksheet.write(0, 1, "Автор", bold)
            worksheet.write(0, 2, "Дата и время", bold)

            worksheet.write(1, 0, task.body)
            worksheet.write(1, 1, task.author.short_name)
            worksheet.write_datetime(1, 2, timezone.make_naive(task.created), date_format)

            worksheet.write(2, 0, "Комментарии:", bold)

            row = 3
            for comment in task.comments.all():
                if not comment.is_archived:
                    worksheet.write(row, 0, comment.body)
                    worksheet.write(row, 1, comment.author.short_name)
                    worksheet.write_datetime(row, 2, timezone.make_naive(comment.created), date_format)
                    row += 1

        workbook.close()

        self.stdout.write(self.style.SUCCESS("Отчёт успешно создан."))
