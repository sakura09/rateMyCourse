from unittest import skipIf
from django.test import TestCase, Client, tag
import json

from rateMyCourse.models import User, Teacher, Course, Comment, MakeComment

TEST_DEBUG_SWITCH = True
SEARCH_FAIL = "Search views not work well."
DOC_INCOMPLETE = "Interface Information incomplete."

class BackBasicTestCase(TestCase):
    # Prepare the database by using fixture.
    fixtures = ["fixture.json"]

    # Support Functions
    def postContainTest(self, url, form, text):
        # Send Request
        #   Specify the interface to test by assigning the url.
        #   With the form attached.
        response = self.client.post(url, form)
                    
        # Response Check
        #   Check the status code(default 200) 
        #   and whether contain text in body.
        try:
            body = json.loads(response.content)
            self.assertEqual(body["status"], 1)
            self.assertContains(response, text)
        except Exception as e:
            print("Body is:", body)
            raise e

    def getJsonBody(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["status"], 1)
        retlist = body["body"]
        return (body, retlist)

    def assertDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            self.assertTrue(key in dicta.keys())
            self.assertEquals(dicta[key], dictb[key])


# Test Cases
@tag("back")
class BackCreateTC(BackBasicTestCase):
    def test_sign_up(self):
        # Send Request & Response Check
        self.postContainTest(
            "/signUp/",
            {
                "username": "test",
                "password": "123",
                "mail": "test@test.com"
            },
            "test"
        )
        # Side Effect Check
        #   Check whether the side effects take place.
        self.assertTrue(
            User.objects.filter(
                username="test", 
                password="123",
                mail="test@test.com"
            ).exists()
        )

    def test_add_teacher_no_website(self):
        self.postContainTest(
            "/addTeacher/",
            {
                "name": "test_teacher_no_website",
                "title": "Only For Test",
            },
            "test_teacher_no_website"
        )
        self.assertTrue(
            Teacher.objects.filter(
                name="test_teacher_no_website",
                title="Only For Test"
            ).exists()
        )

    def test_add_teacher_has_website(self):
        self.postContainTest(
            "/addTeacher/",
            {
                "name": "test_teacher_has_website",
                "title": "Only For Test",
                "website": "www.test.com"
            },
            "test_teacher_has_website"
        )
        self.assertTrue(
            Teacher.objects.filter(
                name="test_teacher_has_website",
                title="Only For Test",
                website="www.test.com"
            ).exists()
        )

    def test_add_course(self):
        self.postContainTest(
            "/addCourse/",
            {
                "name": "test_course",
                "website": "www.test.com",
                "courseID": "999",
                "description": "only for test",
                "courseType": "TESTER",
                "credit": 5
            },
            "test_course"
        )
        self.assertTrue(
            Course.objects.filter(
                name="test_course",
                website="www.test.com",
                course_ID="999",
                description="only for test",
                course_type="TESTER",
                credit=5
            )
        )

    @skipIf(TEST_DEBUG_SWITCH, DOC_INCOMPLETE)
    def test_add_teachCourse(self):
        pass
    
    def test_make_comment(self):
        self.postContainTest(
            "/makeComments/",
            {
                "username": "hong",
                "course_ID": "0",
                "content": "hong test comment"
            },
            "成功"
        )
        self.assertTrue(
            Comment.objects.filter(
                content="hong test comment",
            )
        )
        self.assertTrue(
            MakeComment.objects.filter(
                user__username="hong",
                course__course_ID="0",
                comment__content="hong test comment"
            ).exists()
        )


@tag("back")
class BackUpdateTC(BackBasicTestCase):
    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_update_user(self):
        self.postContainTest(
            "/updateUser/",
            {
                "username": "rbq",
                "role": "Teacher",
                "gender": "Male",
                "selfintroduction": "hhh"
            },
            "rbq"
        )
        self.assertTrue(
            User.objects.filter(
                username="rbq",
                role="Teacher",
                gender="Male",
                selfinstroduction="hhh"
            ).exists()
        )

    def test_edit_comment(self):
        comment_ID = Comment.objects.get(content="rbq").id
        self.postContainTest(
            "/editComments/",
            {
                "comment_ID": comment_ID,
                "content": "changed"
            },
            "成功"
        )
        self.assertTrue(
            MakeComment.objects.filter(
                comment__content="changed"
            ).exists()
        )

@tag("back")
class BackSearchTC(BackBasicTestCase):
    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_teacher_assign(self):
        body, retlist = self.getJsonBody(
            "/searchTeacher/" + "qiang"
        )
        self.assertDictEntry(
            body,
            {
                "length": 1
            }
        )
        self.assertDictEntry(
            retlist[0],
            {
                "name": "qiang",
                "website": "www.qiang.com",
                "title": "First Qiang"
            }
        )

    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_teacher_any(self):
        body, retlist = self.getJsonBody(
            "/searchTeacher/"
        )
        self.assertDictEntry(
            body,
            {
                "length": 2
            }
        )

    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_course_assign(self):
        body, retlist = self.getJsonBody(
            "/searchCourse/" + "如何进牢子"
        )
        self.assertDictEntry(
            body,
            {
                "length": 1
            }
        )
        self.assertDictEntry(
            retlist[0],
            {
                "name": "如何进牢子",
                "website": "www.jubao.com",
                "course_id": 110,
                "description": "很简单",
                "course_type": "必修",
                "credit": 3
            }
        )

    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_course_any(self):
        body, retlist = self.getJsonBody(
            "/searchCourse/"
        )
        self.assertDictEntry(
            body,
            {
                "length": 3
            }
        )

    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_user_assign(self):
        body, retlist = self.getJsonBody(
            "/searchUser/" + "ming"
        )
        self.assertDictEntry(
            body,
            {
                "length": 1
            }
        )
        self.assertDictEntry(
            retlist[0],
            {
                "username": "ming",
                "mail": "ming@test.com",
                "role": "Student",
                "gender": "Male",
                "self_introduction": "mingming"
            }
        )

    @skipIf(TEST_DEBUG_SWITCH, SEARCH_FAIL)
    def test_search_user_any(self):
        body, retlist = self.getJsonBody(
            "/searchUser/"
        )
        self.assertDictEntry(
            body,
            {
                "length": 6
            }
        )

    def test_get_comment(self):
        body, retlist = self.getJsonBody(
            "/getCommentsByCourse/110"
        )
        self.assertEquals(len(retlist), 2)
        # TODO Further Content Check

@tag("back")
class BackAuthTC(BackBasicTestCase):
    @skipIf(TEST_DEBUG_SWITCH, DOC_INCOMPLETE)
    def test_sign_in(self):
        pass