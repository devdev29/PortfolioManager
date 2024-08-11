import { HttpClient } from "@angular/common/http";
import { Component, Injectable, signal } from "@angular/core";
import { AppComponent } from "../app.component";
import { Router } from "@angular/router";
import { catchError, Observable, throwError } from "rxjs";

@Component ({
    selector : 'app-add-asset',
    templateUrl : './add-asset.component.html',
    styleUrls : ['./add-asset.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class AddAssetComponent { 
    public ticker: string = '';
    public account_no: string = '';
    public quantity: number = 0;
    public full_name: string = '';
    public exchange: string = '';
    public mcap: string = 'medium';
    tickerOptions: any[] = [];

    constructor(private http: HttpClient, private app: AppComponent, private router: Router) { }

    errorHandler(error: {
        error: { message: string; };
        status: any; message: any;
    }) {
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            errorMessage = error.error.message;
        } 
        else {
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        return throwError(errorMessage);
    }

    getStockByTicker(ticker: string): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/search/' + ticker).pipe(catchError(this.errorHandler));
    }

    addStock(body: any): Observable<any> {
        return this.http.post(this.app.domain + 'stocks/portfolio', body).pipe(catchError(this.errorHandler));
    }

    searchTicker() {
        this.getStockByTicker(this.ticker).subscribe(data => {
            this.tickerOptions = data;
        });
    }

    addStocks() {
        var body = {
            "ticker": this.ticker,
            "quantity": this.account_no,
            "account_no": this.account_no,
            "exchange": this.exchange,
            "market_cap": this.mcap,
            "full_name": this.full_name
        };

        this.addStock(body).subscribe(data => {
            console.log();
            window.location.reload();
        });
    }
}