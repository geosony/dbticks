import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  menu = 0;
  page = 'login';
  constructor(
    private router: Router,
  ) {}

  ngOnInit() {
  }

  onClickLogin() {
    this.router.navigate(['/dashboard'])
  }

}
