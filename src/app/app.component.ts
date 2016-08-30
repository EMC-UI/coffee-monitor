import {Component} from '@angular/core';
import {CoffeeService} from "./coffee.service";

@Component({
  moduleId: module.id,
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css'],
  providers: [CoffeeService]
})
export class AppComponent {

  title = 'app works!';
  days = [];
  hours = [];
  start = '';
  end = '';

  constructor(private coffeeService: CoffeeService) {
  }

  ngOnInit() {
    this.getDayStats();
    this.getHourStats();
    this.getEndDate();
    this.getStartDate();
  }

  calcPercentage(results) {
    let total = results.reduce((prevVal, curVal) => {
      return prevVal + curVal.count;
    }, 0);
    results.forEach((result) => {
      result.percentage = Math.ceil((result.count / total) * 100);
    });
    return results;
  }

  getDayStats() {
    this.coffeeService.getDayStats().then((days) => {
      this.days = this.calcPercentage(days);
    })
  }

  getHourStats() {
    this.coffeeService.getHourStats().then((hours) => {
      this.hours = this.calcPercentage(hours);
    })
  }

  getEndDate() {
    this.coffeeService.getEndDate().then((response) => { this.end = response });
  }

  getStartDate() {
    this.coffeeService.getStartDate().then((response) => { this.start = response });
  }

}
