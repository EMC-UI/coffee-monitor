import { Injectable } from '@angular/core';
import 'rxjs/add/operator/toPromise';
import {Http} from "@angular/http";
import {DayStats} from "./day-stats";
import {HourStats} from "./hour-stats";

@Injectable()
export class CoffeeService {

  constructor(private http: Http) { }

  private handleError(error: any) {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }

  getDayStats() {
    return this.http.get('http://localhost:3000/day').toPromise()
      .then(response => response.json() as DayStats[])
      .catch(this.handleError);
  }

  getHourStats() {
    return this.http.get('http://localhost:3000/hour').toPromise()
      .then(response => response.json() as HourStats[])
      .catch(this.handleError);
  }

  getStartDate() {
    return this.http.get('http://localhost:3000/start').toPromise()
      .then(response => response.text())
      .catch(this.handleError);
  }

  getEndDate() {
    return this.http.get('http://localhost:3000/end').toPromise()
      .then(response => response.text())
      .catch(this.handleError);
  }

}
