import type { AspidaClient, BasicHeaders } from 'aspida';
import type { Methods as Methods_1kf9dgv } from './admin/quizes';
import type { Methods as Methods_1mpww1d } from './admin/quizes/_quizId';
import type { Methods as Methods_jec7oc } from './python';
import type { Methods as Methods_1q11sg0 } from './python/_userId';
import type { Methods as Methods_xi21t3 } from './quizes';
import type { Methods as Methods_1e7hkeu } from './shop';
import type { Methods as Methods_12iksgo } from './shop/_shop_id';
import type { Methods as Methods_oim4qi } from './shops/_shopId@number/likes';
import type { Methods as Methods_8d8wef } from './shops/_shopId@number/likes/_likeId@number';
import type { Methods as Methods_180bcj9 } from './user/_userId';
import type { Methods as Methods_jafs0w } from './users/_user_id@number/saved_shops';
import type { Methods as Methods_4m31eb } from './users/_user_id@number/saved_shops/_shop_id@number';

const api = <T>({ baseURL, fetch }: AspidaClient<T>) => {
  const prefix = (baseURL === undefined ? 'http://localhost/api/v1' : baseURL).replace(/\/$/, '');
  const PATH0 = '/admin/quizes';
  const PATH1 = '/python';
  const PATH2 = '/quizes';
  const PATH3 = '/shop';
  const PATH4 = '/shops';
  const PATH5 = '/likes';
  const PATH6 = '/user';
  const PATH7 = '/users';
  const PATH8 = '/saved_shops';
  const GET = 'GET';
  const POST = 'POST';
  const PUT = 'PUT';
  const DELETE = 'DELETE';

  return {
    admin: {
      quizes: {
        _quizId: (val2: number | string) => {
          const prefix2 = `${PATH0}/${val2}`;

          return {
            /**
             * @returns 成功
             */
            get: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_1mpww1d['get']['resBody'], BasicHeaders, Methods_1mpww1d['get']['status']>(prefix, prefix2, GET, option).json(),
            /**
             * @returns 成功
             */
            $get: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_1mpww1d['get']['resBody'], BasicHeaders, Methods_1mpww1d['get']['status']>(prefix, prefix2, GET, option).json().then(r => r.body),
            /**
             * @param option.body - クイズ内容
             * @returns 成功
             */
            put: (option: { body: Methods_1mpww1d['put']['reqBody'], config?: T | undefined }) =>
              fetch<Methods_1mpww1d['put']['resBody'], BasicHeaders, Methods_1mpww1d['put']['status']>(prefix, prefix2, PUT, option).json(),
            /**
             * @param option.body - クイズ内容
             * @returns 成功
             */
            $put: (option: { body: Methods_1mpww1d['put']['reqBody'], config?: T | undefined }) =>
              fetch<Methods_1mpww1d['put']['resBody'], BasicHeaders, Methods_1mpww1d['put']['status']>(prefix, prefix2, PUT, option).json().then(r => r.body),
            delete: (option?: { config?: T | undefined } | undefined) =>
              fetch<void, BasicHeaders, Methods_1mpww1d['delete']['status']>(prefix, prefix2, DELETE, option).send(),
            $delete: (option?: { config?: T | undefined } | undefined) =>
              fetch<void, BasicHeaders, Methods_1mpww1d['delete']['status']>(prefix, prefix2, DELETE, option).send().then(r => r.body),
            $path: () => `${prefix}${prefix2}`,
          };
        },
        /**
         * @param option.body - 一問クイズ作成
         * @returns 成功
         */
        post: (option: { body: Methods_1kf9dgv['post']['reqBody'], config?: T | undefined }) =>
          fetch<Methods_1kf9dgv['post']['resBody'], BasicHeaders, Methods_1kf9dgv['post']['status']>(prefix, PATH0, POST, option).json(),
        /**
         * @param option.body - 一問クイズ作成
         * @returns 成功
         */
        $post: (option: { body: Methods_1kf9dgv['post']['reqBody'], config?: T | undefined }) =>
          fetch<Methods_1kf9dgv['post']['resBody'], BasicHeaders, Methods_1kf9dgv['post']['status']>(prefix, PATH0, POST, option).json().then(r => r.body),
        /**
         * @returns 成功
         */
        get: (option?: { config?: T | undefined } | undefined) =>
          fetch<Methods_1kf9dgv['get']['resBody'], BasicHeaders, Methods_1kf9dgv['get']['status']>(prefix, PATH0, GET, option).json(),
        /**
         * @returns 成功
         */
        $get: (option?: { config?: T | undefined } | undefined) =>
          fetch<Methods_1kf9dgv['get']['resBody'], BasicHeaders, Methods_1kf9dgv['get']['status']>(prefix, PATH0, GET, option).json().then(r => r.body),
        $path: () => `${prefix}${PATH0}`,
      },
    },
    python: {
      _userId: (val1: number | string) => {
        const prefix1 = `${PATH1}/${val1}`;

        return {
          get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_1q11sg0['get']['resBody'], BasicHeaders, Methods_1q11sg0['get']['status']>(prefix, prefix1, GET, option).json(),
          $get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_1q11sg0['get']['resBody'], BasicHeaders, Methods_1q11sg0['get']['status']>(prefix, prefix1, GET, option).json().then(r => r.body),
          $path: () => `${prefix}${prefix1}`,
        };
      },
      /**
       * @param option.body - 店内容
       * @returns 成功
       */
      post: (option: { body: Methods_jec7oc['post']['reqBody'], config?: T | undefined }) =>
        fetch<Methods_jec7oc['post']['resBody'], BasicHeaders, Methods_jec7oc['post']['status']>(prefix, PATH1, POST, option).json(),
      /**
       * @param option.body - 店内容
       * @returns 成功
       */
      $post: (option: { body: Methods_jec7oc['post']['reqBody'], config?: T | undefined }) =>
        fetch<Methods_jec7oc['post']['resBody'], BasicHeaders, Methods_jec7oc['post']['status']>(prefix, PATH1, POST, option).json().then(r => r.body),
      /**
       * @returns 成功
       */
      get: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods_jec7oc['get']['resBody'], BasicHeaders, Methods_jec7oc['get']['status']>(prefix, PATH1, GET, option).json(),
      /**
       * @returns 成功
       */
      $get: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods_jec7oc['get']['resBody'], BasicHeaders, Methods_jec7oc['get']['status']>(prefix, PATH1, GET, option).json().then(r => r.body),
      $path: () => `${prefix}${PATH1}`,
    },
    quizes: {
      /**
       * @returns 成功
       */
      get: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods_xi21t3['get']['resBody'], BasicHeaders, Methods_xi21t3['get']['status']>(prefix, PATH2, GET, option).json(),
      /**
       * @returns 成功
       */
      $get: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods_xi21t3['get']['resBody'], BasicHeaders, Methods_xi21t3['get']['status']>(prefix, PATH2, GET, option).json().then(r => r.body),
      $path: () => `${prefix}${PATH2}`,
    },
    shop: {
      _shop_id: (val1: number | string) => {
        const prefix1 = `${PATH3}/${val1}`;

        return {
          /**
           * @returns 成功
           */
          get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_12iksgo['get']['resBody'], BasicHeaders, Methods_12iksgo['get']['status']>(prefix, prefix1, GET, option).json(),
          /**
           * @returns 成功
           */
          $get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_12iksgo['get']['resBody'], BasicHeaders, Methods_12iksgo['get']['status']>(prefix, prefix1, GET, option).json().then(r => r.body),
          $path: () => `${prefix}${prefix1}`,
        };
      },
      /**
       * @returns 成功
       */
      post: (option: { body: Methods_1e7hkeu['post']['reqBody'], config?: T | undefined }) =>
        fetch<Methods_1e7hkeu['post']['resBody'], BasicHeaders, Methods_1e7hkeu['post']['status']>(prefix, PATH3, POST, option).json(),
      /**
       * @returns 成功
       */
      $post: (option: { body: Methods_1e7hkeu['post']['reqBody'], config?: T | undefined }) =>
        fetch<Methods_1e7hkeu['post']['resBody'], BasicHeaders, Methods_1e7hkeu['post']['status']>(prefix, PATH3, POST, option).json().then(r => r.body),
      $path: () => `${prefix}${PATH3}`,
    },
    shops: {
      _shopId: (val1: number) => {
        const prefix1 = `${PATH4}/${val1}`;

        return {
          likes: {
            _likeId: (val3: number) => {
              const prefix3 = `${prefix1}${PATH5}/${val3}`;

              return {
                delete: (option?: { config?: T | undefined } | undefined) =>
                  fetch<void, BasicHeaders, Methods_8d8wef['delete']['status']>(prefix, prefix3, DELETE, option).send(),
                $delete: (option?: { config?: T | undefined } | undefined) =>
                  fetch<void, BasicHeaders, Methods_8d8wef['delete']['status']>(prefix, prefix3, DELETE, option).send().then(r => r.body),
                $path: () => `${prefix}${prefix3}`,
              };
            },
            /**
             * @returns 成功
             */
            post: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_oim4qi['post']['resBody'], BasicHeaders, Methods_oim4qi['post']['status']>(prefix, `${prefix1}${PATH5}`, POST, option).json(),
            /**
             * @returns 成功
             */
            $post: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_oim4qi['post']['resBody'], BasicHeaders, Methods_oim4qi['post']['status']>(prefix, `${prefix1}${PATH5}`, POST, option).json().then(r => r.body),
            $path: () => `${prefix}${prefix1}${PATH5}`,
          },
        };
      },
    },
    user: {
      _userId: (val1: number | string) => {
        const prefix1 = `${PATH6}/${val1}`;

        return {
          /**
           * @returns 成功
           */
          get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_180bcj9['get']['resBody'], BasicHeaders, Methods_180bcj9['get']['status']>(prefix, prefix1, GET, option).json(),
          /**
           * @returns 成功
           */
          $get: (option?: { config?: T | undefined } | undefined) =>
            fetch<Methods_180bcj9['get']['resBody'], BasicHeaders, Methods_180bcj9['get']['status']>(prefix, prefix1, GET, option).json().then(r => r.body),
          $path: () => `${prefix}${prefix1}`,
        };
      },
    },
    users: {
      _user_id: (val1: number) => {
        const prefix1 = `${PATH7}/${val1}`;

        return {
          saved_shops: {
            _shop_id: (val3: number) => {
              const prefix3 = `${prefix1}${PATH8}/${val3}`;

              return {
                delete: (option?: { config?: T | undefined } | undefined) =>
                  fetch<void, BasicHeaders, Methods_4m31eb['delete']['status']>(prefix, prefix3, DELETE, option).send(),
                $delete: (option?: { config?: T | undefined } | undefined) =>
                  fetch<void, BasicHeaders, Methods_4m31eb['delete']['status']>(prefix, prefix3, DELETE, option).send().then(r => r.body),
                $path: () => `${prefix}${prefix3}`,
              };
            },
            /**
             * @returns 成功
             */
            get: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_jafs0w['get']['resBody'], BasicHeaders, Methods_jafs0w['get']['status']>(prefix, `${prefix1}${PATH8}`, GET, option).json(),
            /**
             * @returns 成功
             */
            $get: (option?: { config?: T | undefined } | undefined) =>
              fetch<Methods_jafs0w['get']['resBody'], BasicHeaders, Methods_jafs0w['get']['status']>(prefix, `${prefix1}${PATH8}`, GET, option).json().then(r => r.body),
            /**
             * @returns 成功
             */
            post: (option: { body: Methods_jafs0w['post']['reqBody'], config?: T | undefined }) =>
              fetch<Methods_jafs0w['post']['resBody'], BasicHeaders, Methods_jafs0w['post']['status']>(prefix, `${prefix1}${PATH8}`, POST, option).json(),
            /**
             * @returns 成功
             */
            $post: (option: { body: Methods_jafs0w['post']['reqBody'], config?: T | undefined }) =>
              fetch<Methods_jafs0w['post']['resBody'], BasicHeaders, Methods_jafs0w['post']['status']>(prefix, `${prefix1}${PATH8}`, POST, option).json().then(r => r.body),
            $path: () => `${prefix}${prefix1}${PATH8}`,
          },
        };
      },
    },
  };
};

export type ApiInstance = ReturnType<typeof api>;
export default api;
