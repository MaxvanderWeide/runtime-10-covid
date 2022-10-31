import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {EnvService} from "./env.service";
import {catchError, count, flatMap, interval, Observable, of, retryWhen, throwError} from "rxjs";
import {Injectable} from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class DataService {
    constructor(private http: HttpClient, private env: EnvService) {
    }

    static handleError(error: HttpErrorResponse) {
        let errorMessage = error;
        if (error.hasOwnProperty('error')) {
            errorMessage = error.error.detail ? error.error.detail : error.error;
        }
        if (error.error instanceof ErrorEvent) {
            console.error(`An unexpected error occurred: ${errorMessage}`);
        } else {
            console.error(
                `Backend returned code ${error.status}, body was: ${errorMessage}`);
        }
        return throwError(error);
    }

    static retry(maxRetry = 3, delayMs = 2000) {
        return (src: Observable<any>) => src.pipe(
            retryWhen(_ => {
                console.log(`Retrying ${count} of ${maxRetry}`);
                return interval(delayMs).pipe(
                    flatMap(c => c === maxRetry ? throwError('Max retries reached with no success') : of(c))
                );
            })
        );
    }

    public getStatus(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/status`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

}
