package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"text/tabwriter"
)

var w *tabwriter.Writer

func init() {
	w = tabwriter.NewWriter(os.Stdout, 0, 8, 4, ' ', tabwriter.AlignRight)
}

func printRow(names []string) {
	fmtStr := ""
	for _, name := range names {
		fmtStr += (name + "\t")
	}
	fmt.Fprintf(w, "%s\n", fmtStr)
}

func print() {
	defer w.Flush()
	pythonTools := os.Getenv("PYTHON_TOOLS")
	if pythonTools == "" {
		fmt.Printf("no %q set\n", "PYTHON_TOOLS")
		return
	}

	binDir := filepath.Join(pythonTools, "bin")
	allFiles, err := ioutil.ReadDir(binDir)
	if err != nil {
		log.Fatal(err)
	}

	colsEachRow := 8
	filesPerRow := make([]string, 0, colsEachRow)
	// fmt.Println(len(allFiles))
	for _, file := range allFiles {
		if strings.HasSuffix(file.Name(), ".exe") {
			filesPerRow = append(filesPerRow,
				strings.TrimSuffix(file.Name(), ".exe"))
			if len(filesPerRow) == cap(filesPerRow) {
				printRow(filesPerRow)
				filesPerRow = filesPerRow[:0]
			}
		}
	}

	printRow(filesPerRow)
}

func main() {
	print()
}
