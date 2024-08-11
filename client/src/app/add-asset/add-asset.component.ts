import { HttpClient } from "@angular/common/http";
import { Component, Injectable, signal } from "@angular/core";
import { AppComponent } from "../app.component";
import { Router } from "@angular/router";
import { catchError, Observable, throwError } from "rxjs";
import { PortfolioCash } from "src/model/portfolio-cash.model";

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
    public stock_account_no: string = '';
    public stock_quantity: number = 0;
    public stock_full_name: string = '';
    public stock_exchange: string = '';
    public stock_mcap: string = 'medium';
    public tickerOptions: any[] = [];
    
    public mf_id: number = 0;
    public mf_name: string = '';
    public mf_quantity: number = 0;
    public mf_account_no: string = '';
    public mfOptions: any[] = [];
    
    public active_tab: number = 1;
    public accountList: PortfolioCash[] = [];


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

    getCash(): Observable<any> {
        return this.http.get(this.app.domain + 'accounts/all').pipe(catchError(this.errorHandler));
    }

    getStockByTicker(ticker: string): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/search/' + ticker).pipe(catchError(this.errorHandler));
    }

    addStock(body: any): Observable<any> {
        return this.http.post(this.app.domain + 'stocks/portfolio', body).pipe(catchError(this.errorHandler));
    }

    ngOnInit() {
        // this.getCash().subscribe(data => {
        //     console.log(JSON.stringify(data));
        //     this.accountList = data;
        // });
        this.accountList = [{"account_no":"bbb","account_type":"current","amount":100000,"bank_name":"growww"},{"account_no":"ccc","account_type":"savings","amount":50000,"bank_name":"Share Khan"},{"account_no":"aaa","account_type":"savings","amount":191358.5994,"bank_name":"Zerodha"}];
    }

    searchTicker() {
        this.tickerOptions =[];
        if(this.ticker.length === 0 || this.ticker.length === 1 || this.ticker.length === 2)
            return;
        // this.getStockByTicker(this.ticker.toUpperCase()).subscribe(data => {
        //     console.log(JSON.stringify(data));
        //     this.tickerOptions = data;
        // });
        this.tickerOptions = [{"currency":"USD","exchangeShortName":"NASDAQ","name":"Passage Bio, Inc.","stockExchange":"NASDAQ Global Select","symbol":"PASG"}, {"currency":"USD","exchangeShortName":"NASDAQ","name":"T. Rowe Price Small-Cap Value Fund","stockExchange":"NASDAQ","symbol":"PASVX"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"T. Rowe Price Small-Cap Stock Fund Advisor Class","stockExchange":"NASDAQ","symbol":"PASSX"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Pasithea Therapeutics Corp.","stockExchange":"NASDAQ Capital Market","symbol":"KTTAW"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Pasithea Therapeutics Corp.","stockExchange":"NASDAQ Capital Market","symbol":"KTTA"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"iPass Inc.","stockExchange":"NASDAQ","symbol":"IPAS"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"COMPASS Pathways plc","stockExchange":"NASDAQ Global Select","symbol":"CMPS"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Compass Therapeutics, Inc.","stockExchange":"NASDAQ Capital Market","symbol":"CMPX"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Compass Digital Acquisition Corp.","stockExchange":"NASDAQ Global Market","symbol":"CDAQW"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Compass Digital Acquisition Corp.","stockExchange":"NASDAQ Global Market","symbol":"CDAQU"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Compass Digital Acquisition Corp.","stockExchange":"NASDAQ Global Market","symbol":"CDAQ"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"E-compass Acquisition Corp. - U","stockExchange":"NASDAQ","symbol":"ECACU"},{"currency":"USD","exchangeShortName":"NASDAQ","name":"Society Pass Incorporated","stockExchange":"NASDAQ Capital Market","symbol":"SOPA"}];
        console.log(this.ticker);
    }

    searchMF() {
        this.mfOptions =[];
        // if(this.ticker.length === 0 || this.ticker.length === 1 || this.ticker.length === 2)
        //     return;
        // this.getStockByTicker(this.ticker.toUpperCase()).subscribe(data => {
        //     console.log(JSON.stringify(data));
        //     this.tickerOptions = data;
        // });
        console.log(this.ticker);
    }

    selectTicker(i: number) {
        this.ticker = this.tickerOptions[i].symbol;
        this.stock_full_name = this.tickerOptions[i].name;
        this.stock_exchange = this.tickerOptions[i].exchangeShortName;
        this.tickerOptions = [];
    }

    selectMF(i: number) {
        // this.ticker = this.tickerOptions[i].symbol;
        // this.stock_full_name = this.tickerOptions[i].name;
        // this.stock_exchange = this.tickerOptions[i].exchangeShortName;
        // this.tickerOptions = [];
    }

    fixAccountforStocks(event: any) {
        this.stock_account_no = event.target.value;
        console.log('Selected account:', this.stock_account_no);
    }

    fixAccountforMF(event: any) {
        this.mf_account_no = event.target.value;
        console.log('Selected account:', this.mf_account_no);
    }

    addStocks() {
        var body = {
            "ticker": this.ticker,
            "quantity": this.stock_quantity,
            "account_no": this.stock_account_no,
            "exchange": this.stock_exchange,
            "market_cap": this.stock_mcap,
            "full_name": this.stock_full_name
        };
        console.log(body);
        this.addStock(body).subscribe(data => {
            console.log(JSON.stringify(data));
            window.location.reload();
        });
    }

    addMF() {
        // var body = {
        //     "ticker": this.ticker,
        //     "quantity": this.stock_quantity,
        //     "account_no": this.stock_account_no,
        //     "exchange": this.stock_exchange,
        //     "market_cap": this.stock_mcap,
        //     "full_name": this.stock_full_name
        // };
        // console.log(body);
        // this.addStock(body).subscribe(data => {
        //     console.log(JSON.stringify(data));
        //     window.location.reload();
        // });
    }

    selectTab(val: number) {
        this.active_tab = val;
    }
}