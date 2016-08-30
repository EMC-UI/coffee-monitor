import { CoffeeMonitorPage } from './app.po';

describe('coffee-monitor App', function() {
  let page: CoffeeMonitorPage;

  beforeEach(() => {
    page = new CoffeeMonitorPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
