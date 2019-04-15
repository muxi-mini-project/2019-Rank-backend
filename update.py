# call Update function before rank !!!
from app.models import Student, WeRun, Department
from datetime import date, timedelta
import redis

redis_db = redis.StrictRedis(host="67.216.199.87", port=6379, db=1)


# 图书馆排行
def lib_rank():
    redis_db.delete('lib_rank')
    for student in Student.query.all():
        redis_db.zadd('lib_rank', {student.id: student.booknum})


# 个人步数日排行
def step_person_rank():
    redis_db.delete('step_person_rank')
    for student in Student.query.all():
        redis_db.zadd('step_person_rank', {student.id: 0})
    for student in Student.query.all():
        werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
        if werun:
            redis_db.zadd('step_person_rank', {student.id: werun.step})


# 学院步数周排行
def dep_weekly_rank():
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


# 学院步数月排行
def dep_monthly_rank():
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


def main():
    lib_rank()
    step_person_rank()
    dep_weekly_rank()
    dep_monthly_rank()


if __name__ == '__main__':
    main()
