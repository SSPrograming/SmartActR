// api/reserve.js
/**
 * 预约相关的api
 */
import { request } from './common.js';

const reserve = {
    getAllEquipmentStatus(params) {
        return request({
            url: '/reserve/getAllEquipmentStatus',
            method: 'POST',
            data: params
        });
    },
    getEquipmentStatus(params) {
        return request({
            url: '/reserve/getEquipmentStatus',
            method: 'POST',
            data: params
        });
    },
    reserveEquipment(params) {
        return request({
            url: '/reserve/reserveEquipment',
            method: 'POST',
            data: params
        });
    },
    getCurrentReserveInfo() {
        return request({
            url: '/reserve/getCurrentReserveInfo',
            method: 'GET'
        });
    },
    getHistoryReserveInfo() {
        return request({
            url: '/reserve/getHistoryReserveInfo',
            method: 'GET'
        });
    },
    cancelReserve(params) {
        return request({
            url: '/reserve/cancelReserve',
            method: 'POST',
            data: params
        });
    }
};

export default reserve;
