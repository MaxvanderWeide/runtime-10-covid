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

    public getCases(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/cases`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getDeaths(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/deaths`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getVaccin(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/vaccinations`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getPredictor(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/predictor`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getNewCases(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/new/cases`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getLive(country): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/live/${country}`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getNewDeaths(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/new/deaths`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

    public getNewVaccin(): Observable<any> {
        return this.http.get(`${this.env.apiUrl}/new/vaccinations`)
            .pipe(
                catchError(DataService.handleError)
            );
    }

}
