/**
 * api接口的统一出口
 */
import admin from './admin'
import notice from './notice'
import reserve from './reserve'
import equipment from './equipment'
import qrcode from './qrcode'
import rule from './rule'
import instruction from './instruction'
import user from './user'

export default {
  admin,
  notice,
  reserve,
  equipment,
  qrcode,
  rule,
  instruction,
  user
}
