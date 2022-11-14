
import {Injectable} from '@angular/core';
import {HttpRequest, HttpHandler, HttpEvent, HttpInterceptor} from '@angular/common/http';
import {Observable} from 'rxjs';
import {EnvService} from "../services/env.service";

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  constructor(private envService: EnvService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    request = request.clone({
      setHeaders: {
        'X-Auth': `${this.envService.apiToken}`
      }
    });
    return next.handle(request);
  }
}
