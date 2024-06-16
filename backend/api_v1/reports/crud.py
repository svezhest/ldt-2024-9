"""
Create
Read
Update
Delete
"""

import datetime
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.workload.workload import WorkloadType

from .schemas import Report as ReportSchema
from core.models import Report

from typing import Union


async def get_report(
        doctor_id: int,
        date: datetime.date,
        workload_type: WorkloadType,
        session: AsyncSession) -> ReportSchema:

    report = await session.get(Report, (doctor_id, date, workload_type))

    if not report:
        report = await post_report(
            doctor_id,
            date,
            workload_type,
            0,
            session)
        
        return report

    return ReportSchema(
        doctor_id=report.doctor_id,
        date=report.date,
        workload_type=report.workload_type,
        amount=report.amount
    )


async def get_total_for_week(
        date_from: datetime.date,
        date_to: datetime.date,
        workload_type: WorkloadType,
        session: AsyncSession):

    stmt = select(Report).where(Report.date >= date_from).where(
        Report.date <= date_to).where(Report.workload_type == workload_type)

    result: Result = await session.execute(stmt)

    return sum(report.amount for report in result.scalars().all())


async def post_report(
        doctor_id: int,
        date: datetime.date,
        workload_type: WorkloadType,
        amount: int,
        session: AsyncSession):
    report = await session.get(Report, (doctor_id, date, workload_type))

    if report is None:
        session.add(
            Report(
                doctor_id=doctor_id,
                date=date,
                workload_type=workload_type,
                amount=amount))
    else:
        report.amount = amount

    await session.commit()

    return ReportSchema(
        doctor_id=report.doctor_id,
        date=report.date,
        workload_type=report.workload_type,
        amount=report.amount
    )
