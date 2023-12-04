/* eslint-disable */
import type * as Types from '../@types'

export type Methods = {
  post: {
    status: 201
    /** 成功 */
    resBody: Types.ShopSearch[]
    /** 店内容 */
    reqBody: Types.Keyword
  }

  get: {
    status: 200
    /** 成功 */
    resBody: Types.ShopSearch[]
  }
}
