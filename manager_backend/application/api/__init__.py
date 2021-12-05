from application.api import admin, notice, reserve, equipment, qrcode, rule, user

bp = [admin.bp_admin,notice.bp_notice, reserve.bp_reserve, equipment.bp_equipment, qrcode.bp_qrcode, rule.bp_rule,user.bp_user]