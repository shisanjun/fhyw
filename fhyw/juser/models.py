from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.

class Menu(models.Model):
    """一级菜单表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="菜单名", help_text="一级菜单名")
    seq = models.PositiveSmallIntegerField(verbose_name="序列号", help_text="菜单导航显示的顺序")
    comment = models.TextField(verbose_name="备注", blank=True, null=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "一级菜单"
        verbose_name_plural = "一级菜单"
        db_table = "menu"


class Menu2(models.Model):
    """二级菜单表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="菜单名", help_text="二级菜单名")
    seq = models.PositiveSmallIntegerField(verbose_name="序列号", help_text="菜单导航显示的顺序")
    url_type_choice = (
        (0, "相对URL"),
        (1, "绝对URL"),
    )
    url_type = models.PositiveSmallIntegerField(choices=url_type_choice, default=0, verbose_name="URL类型",
                                                help_text="选择相对URL还是绝对URL")
    url = models.CharField(max_length=128, verbose_name="URL地址", help_text="输入URL地址")
    menu = models.ForeignKey("Menu", verbose_name="选择上级菜单",on_delete=None)
    comment = models.TextField(verbose_name="备注", blank=True, null=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "二级菜单"
        verbose_name_plural = "二级菜单"
        db_table = "menu2"


class Role(models.Model):
    """角色表，用于用户拥有那些菜单功能"""
    name = models.CharField(max_length=64, unique=True, verbose_name="角色名")
    menu = models.ManyToManyField("Menu", verbose_name="分配菜单功能")
    comment = models.TextField(verbose_name="备注", blank=True, null=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色管理"
        verbose_name_plural = "角色管理"
        db_table = "role"


class UserGroup(models.Model):
    """用户组"""
    name = models.CharField(max_length=64, unique=True, verbose_name="用户组名")
    comment = models.TextField(verbose_name="备注", blank=True, null=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户组管理"
        verbose_name_plural = "用户组管理"
        db_table = "usergroup"


class MyUserManager(BaseUserManager):
    def create_user(self, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not name:
            raise ValueError('Users must have an email address')

        user = self.model(
                # email=self.normalize_email(email),
                name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
                name=name,
                password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    name = models.CharField(max_length=64, unique=True, verbose_name="用户名")
    email = models.EmailField(verbose_name='邮箱地址', max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role=models.ManyToManyField("Role")
    objects = MyUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = "userprofile"
