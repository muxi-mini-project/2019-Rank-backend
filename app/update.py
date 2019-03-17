# call Update function before rank !!!
from app.rank import *
from datetime import date, timedelta


# 图书馆排行
def lib_rank():
    redis_db.delete('lib_rank')
    for student in Student.query.all():
        redis_db.zadd('lib_rank', {student.id: student.booknum})


# 个人步数日排行
def step_person_rank():
    redis_db.delete('step_person_rank')
    # WIP clear likes
    for student in Student.query.all():
        werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
        if werun:
            redis_db.zadd('step_person_rank', {student.id: werun.step})


# 学院步数日排行
def dep_daily_rank():
    # WIP clear likes
    redis_db.delete('dep_daily_rank')
    # init data structure
    data = []
    for dept in Department.query.all():
        data.append({
            "step": 0,
            "department_id": dept.id,
            "count": 0,
        })
    for werun in WeRun.query.filter_by(time=date.today().isoformat()):
        student = Student.query.get(werun.user_id)
        data[student.department_id - 1]['step'] += werun.step
        data[student.department_id - 1]['count'] += 1
    # calc avg step
    for item in data:
        item['count'] = item['count'] or 1  # lest divided by zero
        item['step'] = int(item['step'] / item['count'])
        redis_db.zadd('dep_daily_rank', {item['department_id']: item['step']})

# 学院步数周排行
def dep_weekly_rank():
    # WIP clear likes
    redis_db.delete('dep_weekly_rank')
    # init data structure
    data = []
    for dept in Department.query.all():
        data.append({
            "step": 0,
            "department_id": dept.id,
        })
    end = date.today().isoformat()
    start = (date.today() - timedelta(days=7)).isoformat()
    # calc total step
    for werun in WeRun.query.filter(WeRun.time >= start, WeRun.time <= end):
        student = Student.query.get(werun.user_id)
        data[student.department_id - 1]['step'] += werun.step
    # add redis
    for item in data:
        redis_db.zadd('dep_weekly_rank', {item['department_id']: item['step']})

# 学院步数周排行
def dep_monthly_rank():
    # WIP clear likes
    redis_db.delete('dep_monthly_rank')
    # init data structure
    data = []
    for dept in Department.query.all():
        data.append({
            "step": 0,
            "department_id": dept.id,
        })
    end = date.today().isoformat()
    start = (date.today() - timedelta(days=30)).isoformat()
    # calc total step
    for werun in WeRun.query.filter(WeRun.time >= start, WeRun.time <= end):
        student = Student.query.get(werun.user_id)
        data[student.department_id - 1]['step'] += werun.step
    # add redis
    for item in data:
        redis_db.zadd('dep_monthly_rank', {item['department_id']: item['step']})