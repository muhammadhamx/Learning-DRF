class BlogRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'blog_db'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'blog_db'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'blog' and obj2._meta.app_label == 'blog':
            return True
        if obj1._meta.app_label != 'blog' and obj2._meta.app_label != 'blog':
            return True
        return False
    def allow_migrate(self, db, app_label, model_name = None, **hints):
        if app_label == 'blog':
            return db == 'blog_db'
        return db == 'default'
    



# Author.objects.using('blog_db').all()