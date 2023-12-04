/* eslint-disable */
import type * as Types from '../../../@types'

export type Methods = {
  get: {
    status: 200
    /** 成功 */
    resBody: Types.Quiz
  }

  put: {
    status: 201
    /** 成功 */
    resBody: Types.Quiz
    /** クイズ内容 */
    reqBody: Types.Quiz
  }

  delete: {
    status: 204
  }
}
