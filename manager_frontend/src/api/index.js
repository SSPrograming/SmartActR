/**
 * api接口的统一出口
 */
import admin from './admin'
import notice from './notice'
import reserve from './reserve'
import equipment from './equipment'
import qrcode from './qrcode'

export default {
  admin,
  notice,
  reserve,
  equipment,
  qrcode
}
