# coding=utf-8
from . import admin
from flask import render_template, request
from model import DBSession, Task
from flask.ext.login import login_required, current_user
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified


@admin.route('/list_task')
@login_required
def list_task():
    session = DBSession()
    tasks = session.query(Task).order_by(Task.id.desc()).all()
    session.close()
    return render_template('task/list.html', tasks=tasks)


@admin.route('/new_task', methods=['POST', 'GET'])
@login_required
def new_task():
    if request.method == 'GET':
        extend_id = request.args.get('extend_id')
        return render_template('task/new.html')
    else:
        data = request.form
        task = Task(
                name=data.get('task_name'),
                user=current_user.name,
                create_time=datetime.now(),
                command=data.get('command'),
                priority=data.get('priority'),
                machine_pool=data.get('machine_pool').split('\n'),
                father_task=data.get('father_task').split('\n'),
                valid=data.get('valid') == 'true',
                rerun=data.get('rerun') == 'true',
                rerun_times=data.get('rerun_times'),
                scheduled_type=data.get('scheduled_type'),
                year=data.get('year'),
                month=data.get('month'),
                weekday=data.get('weekday'),
                day=data.get('day'),
                hour=data.get('hour'),
                minute=data.get('minute')
        )
        session = DBSession()
        session.add(task)

        father_task = data.get('father_task')

        # 填充父任务的子任务
        # todo:父任务填写错误返回异常
        if father_task is not None and father_task.strip() != '':
            for father_id in father_task.split('\n'):
                father_task = session.query(Task).filter_by(id=father_id).first()
                father_task.child_task.append(str(task.id))
                flag_modified(father_task, "child_task")

        session.commit()
        session.close()
        return '/' if request.form.get('has_next') == 'false' else 'new_task'


@admin.route('/modify_task', methods=['POST', 'GET'])
@login_required
def modify_task():
    if request.method == 'GET':
        extend_id = request.args.get('extend_id')
        return render_template('task/modify.html')
    else:
        pass