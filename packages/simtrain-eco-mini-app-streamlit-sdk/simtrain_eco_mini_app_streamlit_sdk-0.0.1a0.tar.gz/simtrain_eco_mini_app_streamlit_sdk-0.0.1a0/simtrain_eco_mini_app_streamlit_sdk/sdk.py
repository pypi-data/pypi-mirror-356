from .services.ui import UI
from .services.resources.student import Student
from .services.init_message_bridge import InitMessageBridge
from .services.helper import Helper as SimtrainSdkHelper

# ========================== Import Resource ==========================


from .services.resources.tenant import Tenant

from .services.resources.organization import Organization

from .services.resources.branch import Branch

from .services.resources.academy_session import AcademySession

from .services.resources.account_transaction import AccountTransaction

from .services.resources.agent import Agent

from .services.resources.announcement import Announcement

from .services.resources.announcement_type import AnnouncementType

from .services.resources.app_message import AppMessage

from .services.resources.app_user import AppUser

from .services.resources.app_user_announcement_view import AppUserAnnouncementView

from .services.resources.area import Area

from .services.resources.attendance import Attendance

from .services.resources.category import Category

from .services.resources.credit_note import CreditNote

from .services.resources.enrollment import Enrollment

from .services.resources.enrollment_transaction import EnrollmentTransaction

from .services.resources.holiday import Holiday

from .services.resources.invoice import Invoice

from .services.resources.level import Level

from .services.resources.parent import Parent

from .services.resources.payment import Payment

from .services.resources.payment_method import PaymentMethod

from .services.resources.plugin_installation import PluginInstallation

from .services.resources.product import Product

from .services.resources.product_package import ProductPackage

from .services.resources.punch_card import PunchCard

from .services.resources.race import Race

from .services.resources.refund import Refund

from .services.resources.refund_type import RefundType

from .services.resources.religion import Religion

from .services.resources.room import Room

from .services.resources.room_type import RoomType

from .services.resources.schedule import Schedule

from .services.resources.school import School

from .services.resources.stop_enroll import StopEnroll

from .services.resources.stop_reason import StopReason

from .services.resources.student import Student

from .services.resources.student_description import StudentDescription

from .services.resources.student_group import StudentGroup

from .services.resources.student_source import StudentSource

from .services.resources.student_summary import StudentSummary

from .services.resources.teacher import Teacher

from .services.resources.teacher_group import TeacherGroup

from .services.resources.tuition_class import TuitionClass

from .services.resources.user import User


class SimtrainEcoMiniAppStreamlitSdk:
    def __init__(self):
        InitMessageBridge()

        self.ui = UI()

        self.helper = SimtrainSdkHelper

        # ========================== Import Resource ==========================

        self.tenant = Tenant()

        self.organization = Organization()

        self.branch = Branch()

        self.academySession = AcademySession()

        self.accountTransaction = AccountTransaction()

        self.agent = Agent()

        self.announcement = Announcement()

        self.announcementType = AnnouncementType()

        self.appMessage = AppMessage()

        self.appUser = AppUser()

        self.appUserAnnouncementView = AppUserAnnouncementView()

        self.area = Area()

        self.attendance = Attendance()

        self.category = Category()

        self.creditNote = CreditNote()

        self.enrollment = Enrollment()

        self.enrollmentTransaction = EnrollmentTransaction()

        self.holiday = Holiday()

        self.invoice = Invoice()

        self.level = Level()

        self.parent = Parent()

        self.payment = Payment()

        self.paymentMethod = PaymentMethod()

        self.pluginInstallation = PluginInstallation()

        self.product = Product()

        self.productPackage = ProductPackage()

        self.punchCard = PunchCard()

        self.race = Race()

        self.refund = Refund()

        self.refundType = RefundType()

        self.religion = Religion()

        self.room = Room()

        self.roomType = RoomType()

        self.schedule = Schedule()

        self.school = School()

        self.stopEnroll = StopEnroll()

        self.stopReason = StopReason()

        self.student = Student()

        self.studentDescription = StudentDescription()

        self.studentGroup = StudentGroup()

        self.studentSource = StudentSource()

        self.studentSummary = StudentSummary()

        self.teacher = Teacher()

        self.teacherGroup = TeacherGroup()

        self.tuitionClass = TuitionClass()

        self.user = User()
