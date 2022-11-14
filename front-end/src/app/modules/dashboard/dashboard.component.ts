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

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getCases().subscribe(response => {
      this.cases = response;
    })
    this.dataService.getDeaths().subscribe(response => {
      this.deaths = response;
    })
    this.dataService.getVaccin().subscribe(response => {
      this.vaccin = response;
    })
    this.dataService.getPredictor().subscribe(response => {
      this.predictor = response;
    })
  }

  tog() {
    this.toggle = !this.toggle
    if (!this.retData) {
      this.retData = true;
      this.dataService.getNewCases().subscribe(response => {
        this.cCases = response;
      })
      this.dataService.getNewDeaths().subscribe(response => {
        this.cDeaths = response;
      })
      this.dataService.getNewVaccin().subscribe(response => {
        this.cVaccin = response;
      })
    }
  }

}
