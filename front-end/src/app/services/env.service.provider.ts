import {EnvService} from "./env.service";

interface WindowEnv {
    __env?: any;
}

export const EnvServiceFactory = () => {

    const env: EnvService = new EnvService();

    const browserWindow: WindowEnv = (window || {}) as WindowEnv;
    const browserWindowEnv: any = browserWindow.__env || {};

    for (const key in browserWindowEnv) {
        if (browserWindowEnv.hasOwnProperty(key)) {
            env[key] = browserWindow.__env[key];
        }
    }
    return env;
};

export const EnvServiceProvider = {
    provide: EnvService,
    useFactory: EnvServiceFactory,
    deps: [],
};
