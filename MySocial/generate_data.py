import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySocial.settings")

import django
django.setup()

from faker import Faker
import random
from guardian.shortcuts import assign_perm
from post.models import Post

from accounts.models import User

from groups.models import Group

from groups.models import GroupMember

from post.models import Comment

fakegen = Faker()
list_post = list(Post.objects.all())
list_user = list(User.objects.all())
list_group = list(Group.objects.all())


def populate_user(N=5):
    print ""
    for entry in range(N):
        fake_user = User.objects.create_user(username=fakegen.user_name(), email=fakegen.free_email(),
                                                  password="cuho1993")
        list_user.append(fake_user)
        print fake_user
        fake_user.save()


def populate_group(N=10):
    for entry in range(N):
        faker_group = Group(name=fakegen.company(), description=fakegen.paragraph(nb_sentences=random.randint(3, 10),
                                                                                  variable_nb_sentences=True,
                                                                                  ext_word_list=None))
        list_group.append(faker_group)
        print faker_group
        faker_group.save()

        fake_user = random.choice(list_user)
        groupmember = GroupMember(user=fake_user, group=faker_group)
        groupmember.save()
        assign_perm('groups.can_post', fake_user, faker_group)
        assign_perm('groups.can_delete', fake_user, faker_group)
        print "Admin: {} - Group: {} ".format(fake_user, faker_group)
        print fake_user.has_perm("groups.can_post", faker_group)
        print fake_user.has_perm("groups.can_delete", faker_group)


def populate_groupmember(N=50):
    for entry in range(N):
        fake_user = random.choice(list_user)
        faker_group = random.choice(list_group)
        print "User: {} - Group: {} ".format(fake_user, faker_group)
        if not fake_user.has_perm('groups.can_post', faker_group):
            groupmember=GroupMember(user=fake_user, group=faker_group)
            groupmember.save()
            assign_perm('groups.can_post', fake_user, faker_group)
            print "OK"
            print "User: {} - Group: {} ".format(fake_user, faker_group)


def populate_post(N=50):
    for entry in range(N):
        fake_user = random.choice(list_user)
        faker_group = random.choice(list_group)
        if fake_user.has_perm('groups.can_post', faker_group):
            fake_post = Post(user=fake_user, group=faker_group,
                             title=fakegen.paragraph(nb_sentences=1, variable_nb_sentences=True, ext_word_list=None),
                             message=fakegen.paragraph(nb_sentences=random.randint(3, 10),
                                                        variable_nb_sentences=True, ext_word_list=None),
                             created_at=fakegen.iso8601(tzinfo=None))
            print "{} - user: {} - group: {}".format(fake_post.title, fake_user, faker_group)

            list_post.append(fake_post)
            fake_post.save()


def populate_comment(N=100):
    for entry in range(N):
        fake_post = random.choice(list_post)
        fake_author = fakegen.user_name()
        fake_content = fakegen.text(max_nb_chars=200, ext_word_list=None)
        comment = Comment(post=fake_post, author=fake_author, message=fake_content)
        comment.save()
        print comment


if __name__ == "__main__":
    populate_user()
    populate_group()
    populate_groupmember()
    populate_post()
    populate_comment()
