import { type NuxtAxiosInstance } from "@nuxtjs/axios";
import { Context } from "@nuxt/types";
import { loadCache } from "../repositories";
import { loadErrorHandler } from "../repositories/AxiosErrorHandler";

type PublicAxiosConfig = {
  enableErrors: boolean;
  removeAuthorizationHeader?: boolean;
};

export interface PublicNuxtAxiosInstance extends NuxtAxiosInstance {
  makePublic: (config?: PublicAxiosConfig) => NuxtAxiosInstance;
}

export const useAxiosExtension = (context: Context) => {
  const makePublic = (config: PublicAxiosConfig) => {
    const $axios = context.$axios.create({
      withCredentials: false,
    });

    if (config.enableErrors) {
      loadErrorHandler({
        ...context,
        $axios,
      });
    }

    // Remove Authorization header for get requests if specified
    if (config.removeAuthorizationHeader) {
      const originalGet = $axios.get;
      $axios.get = function(...args) {
        const config = args[1] || {};
        if (!config.headers) {
          config.headers = {};
        }
        config.headers['Authorization'] = undefined;
        args[1] = config;
        return originalGet.apply(this, args);
      };
    }

    loadCache($axios);

    return $axios;
  };

  const create = () => {
    return {
      ...context.$axios,
      makePublic: (
        config: PublicAxiosConfig = {
          enableErrors: true,
          removeAuthorizationHeader: false
        }
      ) => makePublic(config),
    } as PublicNuxtAxiosInstance;
  };

  return create;
};
