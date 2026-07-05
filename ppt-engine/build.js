const pptxgen = require("pptxgenjs");
const fs = require("fs");

const input = process.argv[2];
const output = process.argv[3];

const md = fs.readFileSync(input, "utf8");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Hermes V2";
pptx.subject = "AI Generated";
pptx.title = "Hermes Report";

const slide = pptx.addSlide();

slide.addText("Hermes V2 Report", {
    x:0.5,
    y:0.3,
    w:12,
    h:0.5,
    fontSize:24,
    bold:true
});

slide.addText(md, {
    x:0.5,
    y:1.0,
    w:12,
    h:6,
    fontSize:16,
    breakLine:true
});

pptx.writeFile({ fileName: output });
