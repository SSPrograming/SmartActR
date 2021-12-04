from application.api import admin, notice, reserve, equipment, qrcode, rule

bp = [admin.bp_admin,notice.bp_notice, reserve.bp_reserve, equipment.bp_equipment, qrcode.bp_qrcode, rule.bp_rule]