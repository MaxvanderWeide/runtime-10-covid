import {Component, HostListener} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor() {
  }

  public networkMessage = '';

  @HostListener('window:offline', ['$event'])
  offline() {
    this.networkMessage = 'offline';
  }

  @HostListener('window:online', ['$event'])
  online() {
    this.networkMessage = 'online';
    setTimeout(() => {
      this.networkMessage = '';
    }, 5000);
  }
}
