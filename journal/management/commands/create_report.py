import os
from datetime import datetime

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

import xlsxwriter

from users.models import CustomUser
from core.models import Notification
from journal.models import Task, Report

REPORTS_SUBDIR = "reports"
REPORTS_FULL_PATH = os.path.join(settings.MEDIA_ROOT, REPORTS_SUBDIR)


class Command(BaseCommand):
    """
    Генерирует файл Excel, в который выводятся активные на текущий момент задачи (каждая задача на отдельном листе)
    и все комментарии к ним. К файлу отчета создаётся запись в БД, и рассылаются уведомления о генерации отчета.
    """
    help = "Создаёт отчет `О передаче смены` по текущим задачам и комментариям к ним в формате Excel."

    def handle(self, *args, **options):
        filename = "Report_" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".xlsx"
        report_path = os.path.join(REPORTS_FULL_PATH, filename)

        if not os.path.exists(REPORTS_FULL_PATH):
            os.mkdir(REPORTS_FULL_PATH)

        # Filter all active task and task completed today
        tasks = Task.objects.filter(
            Q(is_private=False, is_completed=False, is_archived=False) |
            Q(is_private=False, is_completed=True, is_archived=False,
              completed__year=timezone.now().year, completed__month=timezone.now().month,
              completed__day=timezone.now().day)
        ).order_by("is_completed", "-completed", "-created")

        # Create Excel file with active tasks and comments
        workbook = xlsxwriter.Workbook(report_path)
        bold = workbook.add_format({"bold": True})
        date_format = workbook.add_format({"num_format": "dd.mm.yyyy hh:mm"})
        date_format_header = workbook.add_format({"num_format": "dd.mm.yyyy hh:mm"})
        date_format_header.set_bg_color("#8ecae6")
        cell_format_wrap = workbook.add_format()
        cell_format_wrap.set_text_wrap()
        cell_format_header = workbook.add_format({"bold": True})
        cell_format_header.set_bg_color("#8ecae6")

        for i, task in enumerate(tasks):
            print(task)
            worksheet = workbook.add_worksheet(name="{num}. {title}".format(
                num=i + 1,
                title=task.title[:26]  # max len = 31
            ))

            worksheet.set_column(0, 0, 100)
            worksheet.set_column(1, 2, 15)

            worksheet.write(0, 0, task.title, cell_format_header)
            worksheet.write(0, 1, "Автор", cell_format_header)
            worksheet.write(0, 2, "Дата и время", cell_format_header)

            worksheet.write(1, 0, task.body, cell_format_wrap)
            worksheet.write(1, 1, task.author.short_name)
            worksheet.write_datetime(1, 2, timezone.make_naive(task.created), date_format)

            worksheet.write(2, 0, "Комментарии:", cell_format_header)
            worksheet.write(2, 1, "", cell_format_header)
            worksheet.write(2, 2, "", cell_format_header)

            row = 3
            for comment in task.comments.all():
                if not comment.is_archived:
                    worksheet.write(row, 0, comment.body, cell_format_wrap)
                    worksheet.write(row, 1, comment.author.short_name)
                    worksheet.write_datetime(row, 2, timezone.make_naive(comment.created), date_format)
                    row += 1

            if task.is_completed and task.completed:
                worksheet.write(row, 0, "Задача завершена: ", cell_format_header)
                worksheet.write(row, 1, "", cell_format_header)
                worksheet.write_datetime(row, 2, timezone.make_naive(task.completed), date_format_header)

        workbook.close()

        # Create Report entry
        report = Report()
        report.title = "Передача смены на {date_time}".format(
            date_time=datetime.now().strftime("%H:%M %d.%m.%Y")
        )
        report.attachment.name = "/{subdir}/{filename}".format(
            subdir=REPORTS_SUBDIR,
            filename=filename
        )
        report.save()

        # Send notification to all users
        # Set an admin as notification sender and actor
        sender = CustomUser.objects.filter(is_superuser=True).first()
        Notification.send(sender=sender, actor=sender, recipient=CustomUser.objects.all(),
                          verb_code=Notification.VERB_CODES.report_add, target=report)

        self.stdout.write(self.style.SUCCESS("Отчёт успешно создан."))
