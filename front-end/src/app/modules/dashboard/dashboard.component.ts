import {AfterViewInit, Component, OnInit} from '@angular/core';
import {DataService} from "../../services/data.service";

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

    public cases = [];
    public deaths = [];
    public vaccin = [];
    public predictor = [];


    public cCases = [];
    public cDeaths = [];
    public cVaccin = [];

    public retData = false;
    public toggle = true;

    public loading = true;

    public live = [];

    constructor(private dataService: DataService) {
    }

    ngOnInit(): void {
        this.dataService.getLive('netherlands').subscribe(response => {
            this.live.push(
                {
                    name: 'netherlands',
                    cases: response.cases,
                    updated: response.date,
                    deaths: response.deaths
                }
            );
        });
        this.dataService.getLive('brazil').subscribe(response => {
            this.live.push(
                {
                    name: 'brazil',
                    cases: response.cases,
                    updated: response.date,
                    deaths: response.deaths
                }
            );
        });
        this.dataService.getLive('spain').subscribe(response => {
            this.live.push(
                {
                    name: 'spain',
                    cases: response.cases,
                    updated: response.date,
                    deaths: response.deaths
                }
            );
        });
        this.dataService.getLive('norway').subscribe(response => {
            this.live.push(
                {
                    name: 'norway',
                    cases: response.cases,
                    updated: response.date,
                    deaths: "No measurement"
                }
            );
        });


        this.dataService.getCases().subscribe(response => {
            this.cases = response;
        });
        this.dataService.getDeaths().subscribe(response => {
            this.deaths = response;
        });
        this.dataService.getVaccin().subscribe(response => {
            this.vaccin = response;
        });
        this.dataService.getPredictor().subscribe(response => {
            this.predictor = response;
            this.loading = false;
        });
    }

    tog() {
        this.toggle = !this.toggle
        if (!this.retData) {
            this.retData = true;
            this.dataService.getNewCases().subscribe(response => {
                this.cCases = response;
            });
            this.dataService.getNewDeaths().subscribe(response => {
                this.cDeaths = response;
            });
            this.dataService.getNewVaccin().subscribe(response => {
                this.cVaccin = response;
            });
        }
    }

}
