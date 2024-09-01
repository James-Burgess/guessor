package main

import (
    "fmt"
    "net/http"
    "sync"
    "time"
    "github.com/cheggaaa/pb/v3"
)

const (
    batchSize  = 1000
    wordSize   = 4
    maxWorkers = 16
    baseURL    = "https://jbx.co.za"
    maxConcurrentRequests = 400
)

func generateWords() []string {
    alphabet := "abcdefghijklmnopqrstuvwxyz"
    var words []string

    var generate func(prefix string, depth int)
    generate = func(prefix string, depth int) {
        if depth == 0 {
            words = append(words, prefix)
            return
        }
        for _, char := range alphabet {
            generate(prefix+string(char), depth-1)
        }
    }

    generate("", wordSize)
    return words
}

func tryWord(client *http.Client, word string, resultChan chan<- result) {
    url := fmt.Sprintf("%s/guess/%s", baseURL, word)
    start := time.Now()
    resp, err := client.Get(url)
    if err != nil {
        resultChan <- result{word, 0, 0, err} // Handle errors
        return
    }
    defer resp.Body.Close()
    duration := time.Since(start)
    resultChan <- result{word, resp.StatusCode, duration, nil}
}

type result struct {
    word        string
    statusCode  int
    duration    time.Duration
    err         error
}

func bruteForceAPI() string {
//     totalWords := 1 << uint(2*wordSize) // 26^wordSize
    bar := pb.StartNew(456976)

    words := generateWords()
    resultChan := make(chan result)
    var wg sync.WaitGroup

    startTime := time.Now()
    wordsTried := 0
    totalDuration := time.Duration(0)

    maxDuration := time.Duration(0)
    minDuration := time.Duration(1<<63 - 1) // Max int64

    maxRPS := 0.0
    minRPS := 1000000.0

    semaphore := make(chan struct{}, maxConcurrentRequests)

	go func() {
		for _, word := range words {
			semaphore <- struct{}{} // Acquire a semaphore slot

			wg.Add(1)
			go func(word string) {
				defer wg.Done()
				tryWord(http.DefaultClient, word, resultChan)
				<-semaphore // Release the semaphore slot
			}(word)
		}
		wg.Wait()
		close(resultChan)
	}()

    for res := range resultChan {
        if res.err != nil {
            bar.Finish()
            fmt.Printf("\nError: %v\n", res.err)
            return ""
        }

        wordsTried++
        bar.Increment()

        elapsed := time.Since(startTime)
        rps := float64(wordsTried) / elapsed.Seconds()
        totalDuration += res.duration
        avgDuration := totalDuration / time.Duration(wordsTried)

        if rps > maxRPS {
            maxRPS = rps
        }
        if rps < minRPS {
            minRPS = rps
        }

        if avgDuration > maxDuration {
            maxDuration = avgDuration
        }
        if avgDuration < minDuration {
            minDuration = avgDuration
        }

        bar.Set("RPS", fmt.Sprintf("%.2f", rps))
        bar.Set("Last", res.word)
        bar.Set("req_avg", fmt.Sprintf("%.2f", avgDuration.Seconds()))

        if res.statusCode == http.StatusOK {
            bar.Finish()
            fmt.Printf("\nSuccess! The correct word is: %s\n", res.word)
            fmt.Printf("The time took to guess the word was: %.2f seconds\n", elapsed.Seconds())
            fmt.Printf("The average request duration was: %.2f seconds\n", avgDuration.Seconds())
            fmt.Printf("The longest request duration was: %.2f seconds\n", maxDuration.Seconds())
            fmt.Printf("The shortest request duration was: %.2f seconds\n", minDuration.Seconds())
            fmt.Printf("The requests per second was: %.2f\n", rps)
            fmt.Printf("The max requests per second was: %.2f\n", maxRPS)
            fmt.Printf("The min requests per second was: %.2f\n", minRPS)
            return res.word
        } else if res.statusCode != http.StatusBadRequest {
            bar.Finish()
            fmt.Printf("\nUnexpected status code: %d\n", res.statusCode)
            return ""
        }
    }

    bar.Finish()
    fmt.Println("\nNo successful guess found")
    return ""
}

func main() {
    result := bruteForceAPI()
    if result != "" {
        fmt.Println("Found:", result)
    }
}
