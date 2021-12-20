// api/api.js
/**
 * api接口的统一出口
 */
import user from './user';
import reserve from './reserve'
import instruction from './instruction'

export default {
  user,
  reserve,
  instruction,
};
