import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'fe';
  page = 'index';
  menu = 1;

  constructor(
    private router: Router
  ) {}

  ngOnInit() {

    this.router.events.subscribe((event) => {
      if(event instanceof NavigationEnd ){
        if (event.url === '/login') {
          this.menu = 0;
        } else {
          this.menu = 1;
        }
        this.page = event.url.slice(1);
      }
    });
  }

  onClickMenu(page: string) {
    this.page = page;
    this.router.navigate(['/' + page])
  }

}
