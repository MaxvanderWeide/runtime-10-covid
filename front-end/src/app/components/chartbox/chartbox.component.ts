import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-chartbox',
  templateUrl: './chartbox.component.html',
  styleUrls: ['./chartbox.component.scss']
})
export class ChartboxComponent implements OnInit {

  @Input() highlighted = false;

  constructor() { }

  ngOnInit(): void {
  }

}
