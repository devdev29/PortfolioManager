import { DatePipe } from "@angular/common";
import { Component } from "@angular/core";
import { faUser } from "@fortawesome/free-solid-svg-icons";

@Component ({
    selector : 'app-header',
    templateUrl : './header.component.html',
    styleUrls : ['./header.component.css'],
    providers: [DatePipe]
})

export class HeaderComponent {
    
    public currentDateTime: any;
    public faUser = faUser;
    public customer: string = "Isika Samanta";

    constructor(private datePipe: DatePipe) {}
    
    ngOnInit(): void {
        this.updateTime();
        setInterval(() => this.updateTime(), 30000); 
    }
    
    updateTime() {
        const now = new Date();
        const date = now.toLocaleDateString(); 
        const time = now.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        this.currentDateTime = `${date} ${time}`; 
    }
}