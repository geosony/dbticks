import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";

@Component({
  selector: 'app-addticket',
  templateUrl: './addticket.component.html',
  styleUrls: ['./addticket.component.css']
})
export class AddticketComponent implements OnInit {

  myForm = new FormGroup({
    title: new FormControl(null, [Validators.required, Validators.minLength(3)]),
    jiraID: new FormControl(null, [Validators.required, Validators.minLength(5)]),
    status: new FormControl(0, [Validators.required]),
    repDate: new FormControl(null, [Validators.required]),
    module: new FormControl(null),
    team: new FormControl(0),
    file: new FormControl(null, [Validators.required]),
    fileSource: new FormControl(null, [Validators.required])
  });

  selectedFile:any;
  constructor(
    private router: Router,
    private http: HttpClient
  ) { }

  ngOnInit(): void {
  }
  get f(){
    return this.myForm.controls;
  }

  onClickBack(page: string) {
    this.router.navigate(['/' + page])
  }

  onChangeFile(event: any) {
    this.selectedFile = event.target.files[0];
    this.myForm.patchValue({
      fileSource: this.selectedFile
    });
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('title', this.myForm.get('title')!.value);
    formData.append('jiraID', this.myForm.get('jiraID')!.value);
    formData.append('status', this.myForm.get('status')!.value);
    formData.append('date', this.myForm.get('repDate')!.value);
    formData.append('module', this.myForm.get('module')!.value);
    formData.append('team', this.myForm.get('team')!.value);
    formData.append('file', this.myForm.get('fileSource')!.value);
    console.log(formData);

    this.http.post(`${environment.serviceUrl}api/upload`, formData)
      .subscribe(res => {
        alert('Uploaded Successfully.');
      })
  }

  changeEvent(e:any) {
    const date = new Date(e.value);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = (date.getDate()).toString().padStart(2, '0');
    const hour = (date.getHours()).toString().padStart(2, '0');
    const minute = (date.getMinutes()).toString().padStart(2, '0');
    const second = (date.getSeconds()).toString().padStart(2, '0');

    const dateStr = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
    this.myForm.patchValue({'repDate': dateStr });
  }

}

