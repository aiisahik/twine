import { TwinePage } from './app.po';

describe('twine App', () => {
  let page: TwinePage;

  beforeEach(() => {
    page = new TwinePage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
