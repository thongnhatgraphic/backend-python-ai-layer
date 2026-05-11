from sqlmodel import Session
from sqlmodel import select, text
from app.models.task_model import Task
from uuid import UUID
from datetime import datetime
import math

from app.response_schema.task_schema import TaskResponse



class TaskRepository: 
    def __init__(self, session: Session):
        self.session = session = session

    def get_tasks_raw(self, 
                      user_id: UUID,
                      page,
                      limit,
                      status,
                      priority,
                      progress,
                      search,
                      sort_by,
                      order
                      ):
        conditions = ['user_id = :user_id']
        params = {'user_id': user_id}

        if status:
            conditions.append('status = :status')
            if status == 'completed':
                params['status'] = 'completed'
            else:
                params['status'] = 'pending'

        if search:
            conditions.append("(name ILIKE :search OR description ILIKE :search)")
            params['search'] = f"%{search}%"

        if priority is not None:
            conditions.append('priority = :priority')
            params['priority'] = priority
        
        if progress:
            conditions.append('progress = :progress')
            params['progress'] = progress

        print('conditions', conditions)

        where_clause = ' AND '.join(conditions)

        order_clause = 'created_at DESC'

        orders = ['created_at', 'updated_at']
        if sort_by in orders:
            if order == 'asc':
                order_clause = f"{sort_by} ASC"
            else:
                order_clause = f"{sort_by} DESC"

        params["limit"] = limit 
        params["offset"] = (page - 1) * limit

        query = text(f"""
            SELECT *
            FROM task
            WHERE {where_clause}
            ORDER BY {order_clause}
            LIMIT :limit OFFSET :offset
        """).bindparams(**params)

        params_copy = params.copy()
        params_copy.pop("limit")
        params_copy.pop("offset")

        count_query = text(f"""
            SELECT COUNT(*) 
            FROM task 
            WHERE {where_clause}
        """).bindparams(**params_copy)
        
        total = self.session.exec(count_query).scalar()

        rows = self.session.exec(query).all()
        return {
            "tasks": [Task(**row._mapping) for row in rows],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": math.ceil(total / limit)
        }

    def get_all(self, 
                user_id: UUID, 
                page, 
                limit, 
                status, 
                priority, 
                search, 
                sort_by, 
                order):
        query = select(Task).where(Task.user_id == user_id)

        sort_column = getattr(Task, sort_by, Task.created_at)
        if order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        

        if (search):
            query = query.where(Task.name.ilike(f"%{search}%"))
            
        if status:
            query = query.where(Task.status == status)

        if priority:
            query = query.where(Task.priority == priority)


        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        return self.session.exec(query).all()    

        # return self.session.exec(
        #     select(Task)
        #     .where(Task.user_id == user_id)
        #     ).all()

    def get_tasks_scale_raw(self, 
                            cursor_created_at,
                            cursor_id,
                            limit, 
                            status, 
                            priority, 
                            search, 
                            user_id: UUID):

        conditions = ['user_id = :user_id']
        params = { 'user_id': user_id }

        if status: 
            conditions.append('status = :status')
            params['status'] = status

        if priority is not None:
            conditions.append('priority = :priority')
            params['priority'] = priority

        if cursor_created_at is not None and cursor_id is not None:
            conditions.append('(created_at, id) < (:cursor_created_at, :cursor_id)')
            params['cursor_created_at'] = cursor_created_at
            params['cursor_id'] = cursor_id

        if search:
            conditions.append("""
                to_tsvector('english', name || ' ' || description)
                @@
                plainto_tsquery(:search)               
            """)
            params["search"] = search.trip()

        params["limit"] = limit

        where_clause = ' AND '.join(conditions)

        query = text(f"""
            SELECT *
            FROM task
            WHERE {where_clause}
            ORDER BY created_at DESC, id DESC
            LIMIT :limit
            """).bindparams(**params)
        

        rows = self.session.exec(query).all()

        next_cursor = None
        if rows:
            last = rows[-1]
            next_cursor = {
                "created_at": last.created_at.isoformat(),
                "id": last.id
            }
        
        return {
                "tasks": [Task(**row._mapping) for row in rows],
                "next_cursor": next_cursor
            }


    def get_by_id_and_user_id_raw(self, task_id, user_id: UUID):
        statement = text("""
            SELECT * FROM task
            WHERE id = :task_id AND user_id = :user_id
        """).bindparams(task_id=task_id, user_id=user_id)
        
        return self.session.exec(statement).first()

    def get_by_id_and_user_id(self, task_id, user_id: UUID):
        return self.session.exec(
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        ).first()
    
    def create_raw(self, task: Task):
        params = {
            "name": task.name,
            "status": task.status,
            "description": task.description,
            "progress": task.progress,
            "priority": task.priority,
            "deadline": task.deadline,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user_id": task.user_id
        }
        print('\n \n \n \n \n params \n \n \n \n \n ', params)
        query = text("""
            INSERT INTO task(
                name, status, description, progress,
                priority, deadline, created_at,
                updated_at, user_id
            )
            VALUES (
                :name, :status, :description, :progress,
                :priority, :deadline, :created_at,
                :updated_at, :user_id
            )
            RETURNING *
        """)

        result = self.session.exec(query.params(**params))
        row = result.first()

        self.session.commit()

        data = dict(row._mapping)
        print('data',data)
        return TaskResponse(**data)

    def create(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update_raw(self, task: Task, name, progress, updated_at, user_id):
        params = {
            "name": name,
            "status": task.status,
            "description": task.description,
            "progress": progress,
            "priority": task.priority,
            "deadline": task.deadline,
            "updated_at": updated_at,
            "task_id": task.id,
            "user_id": user_id
        }
        print('params params', params)
        statement = text("""
            UPDATE task
            SET name = :name, 
                status = :status,
                description = :description,
                progress = :progress,
                priority = :priority,
                deadline = :deadline,
                updated_at = :updated_at
            WHERE id = :task_id AND user_id = :user_id           
            RETURNING *    
            """).bindparams(**params)
        
        result = self.session.exec(statement)
        print("result ------->", result)
        row = result.first()
        print("row ------->", row)
        self.session.commit()
        data = dict(row._mapping)
        print('data ------->",',data)
        return TaskResponse(**data)

    def update(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def delete_raw(self, task_id, user_id: UUID):
        statement = text("""
            DELETE FROM task
            WHERE id=:task_id AND user_id=:user_id
            RETURNING *
        """).bindparams(task_id=task_id, user_id=user_id)

        result = self.session.exec(statement)
        row = result.first()
        self.session.commit()
        data = dict(row._mapping)

        return TaskResponse(**data)
    
    def delete(self, task: Task):
        self.session.delete(task)
        self.session.commit()

    def complete_multiple_tasks(self, task_ids, user_id: UUID):
        try:
            results = []
            
            # Solution 1
            # for task_id in task_ids:
            #     statement = text("""
            #         UPDATE task
            #         SET status = 'completed', progress = 100
            #         WHERE id=:task_id AND user_id=:user_id
            #         RETURNING *
            #     """).bindparams(task_id = int(task_id), user_id=user_id)
            #     result = self.session.exec(statement)
            #     row = result.first()

            #     if row:
            #         results.append(TaskResponse(**dict(row._mapping)))
            
            # self.session.commit()
            # return results

            # Solution 2 Pro
            statement = text(
                """
                UPDATE task
                SET status = 'completed', progress = 100
                WHERE id = ANY(:task_ids) AND user_id = :user_id
                RETURNING *
                """
            ).bindparams(task_ids=task_ids, user_id=user_id)

            rows = self.session.exec(statement).all()
            self.session.commit()

            return [dict(row._mapping) for row in rows]
            
        except Exception as e:
            self.session.rollback()
            raise e

        
