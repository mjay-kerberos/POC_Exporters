import (
	"database/sql"
	"fmt"
	"net/http"
	"os/exec"
	"strconv"
	"strings"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var db *sql.DB

func initDatabase() {
	var err error
	db, err = sql.Open("sqlite3", "utilization.db")
	if err != nil {
		fmt.Printf("ERROR: Failed to open database: %s\n", err)
		return
	}

	createTable := `
	CREATE TABLE IF NOT EXISTS utilization_reports (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		period TEXT, 
		account TEXT,
		cpu_hours FLOAT,
		gpu_hours FLOAT,
		storage_usage_gb FLOAT
	);`

	_, err = db.Exec(createTable)
	if err != nil {
		fmt.Printf("ERROR: Failed to create table: %s\n", err)
	}
}

var (
	weeklyCPUUsage = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "weekly_cpu_usage_hours",
		Help: "Total CPU hours used in the last week per account.",
	}, []string{"account"})

	monthlyCPUUsage = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "monthly_cpu_usage_hours",
		Help: "Total CPU hours used in the last month per account.",
	}, []string{"account"})

	weeklyGPUUsage = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "weekly_gpu_usage_hours",
		Help: "Total GPU hours used in the last week per account.",
	}, []string{"account"})

	monthlyGPUUsage = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "monthly_gpu_usage_hours",
		Help: "Total GPU hours used in the last month per account.",
	}, []string{"account"})

	weeklyStorageUsage = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "weekly_ddn_storage_usage_gb",
		Help: "Total DDN storage used in the last week.",
	})

	monthlyStorageUsage = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "monthly_ddn_storage_usage_gb",
		Help: "Total DDN storage used in the last month.",
	})
)

func registerPrometheusMetrics() {
	prometheus.MustRegister(weeklyCPUUsage)
	prometheus.MustRegister(monthlyCPUUsage)
	prometheus.MustRegister(weeklyGPUUsage)
	prometheus.MustRegister(monthlyGPUUsage)
	prometheus.MustRegister(weeklyStorageUsage)
	prometheus.MustRegister(monthlyStorageUsage)
}

func updatePrometheusMetrics() {
	rows, _ := db.Query("SELECT period, account, SUM(cpu_hours), SUM(gpu_hours), AVG(storage_usage_gb) FROM utilization_reports GROUP BY period, account")
	defer rows.Close()

	for rows.Next() {
		var period, account string
		var cpuHours, gpuHours, storageUsage float64

		rows.Scan(&period, &account, &cpuHours, &gpuHours, &storageUsage)

		if period == "7days" {
			weeklyCPUUsage.WithLabelValues(account).Set(cpuHours)
			weeklyGPUUsage.WithLabelValues(account).Set(gpuHours)
			weeklyStorageUsage.Set(storageUsage)
		} else if period == "30days" {
			monthlyCPUUsage.WithLabelValues(account).Set(cpuHours)
			monthlyGPUUsage.WithLabelValues(account).Set(gpuHours)
			monthlyStorageUsage.Set(storageUsage)
		}
	}
}

func collectUtilization(period string) {
	// Run sreport to get CPU & GPU utilization
	cmd := exec.Command("bash", "-c", fmt.Sprintf("sreport cluster AccountUtilizationByUser start=-%s format=Account,CPU_Hours,GPU_Hours", period))
	output, err := cmd.Output()
	if err != nil {
		fmt.Printf("ERROR: Failed to get %s utilization data: %s\n", period, err)
		return
	}

	lines := strings.Split(strings.TrimSpace(string(output)), "\n")

	// Fetch Storage Utilization
	storageUsage := getDDNStorageUsage()

	for _, line := range lines[1:] { // Skip the header row
		parts := strings.Fields(line)
		if len(parts) < 3 {
			continue
		}

		account := parts[0]
		cpuHours, err := strconv.ParseFloat(parts[1], 64)
		if err != nil {
			fmt.Printf("WARN: Failed to parse CPU hours for account %s: %s\n", account, err)
			continue
		}
		gpuHours, err := strconv.ParseFloat(parts[2], 64)
		if err != nil {
			fmt.Printf("WARN: Failed to parse GPU hours for account %s: %s\n", account, err)
			continue
		}

		_, err = db.Exec("INSERT INTO utilization_reports (period, account, cpu_hours, gpu_hours, storage_usage_gb) VALUES (?, ?, ?, ?, ?)",
			period, account, cpuHours, gpuHours, storageUsage)
		if err != nil {
			fmt.Printf("ERROR: Failed to insert utilization data: %s\n", err)
		}
	}
}

func getDDNStorageUsage() float64 {
	cmd := exec.Command("df", "-BG", "/ddn") // Replace "/ddn" with actual DDN mount point
	output, err := cmd.Output()
	if err != nil {
		fmt.Printf("ERROR: Failed to get DDN storage usage: %s\n", err)
		return 0.0
	}

	lines := strings.Split(strings.TrimSpace(string(output)), "\n")
	if len(lines) < 2 {
		return 0.0
	}

	// Parse the second line of `df -BG` output
	parts := strings.Fields(lines[1])
	if len(parts) < 4 {
		return 0.0
	}

	usedStorage := strings.TrimSuffix(parts[2], "G") // Remove 'G' from size
	usedStorageFloat, err := strconv.ParseFloat(usedStorage, 64)
	if err != nil {
		fmt.Printf("ERROR: Failed to parse DDN storage usage: %s\n", err)
		return 0.0
	}

	return usedStorageFloat
}

func scheduleUtilizationCollection() {
	weeklyTicker := time.NewTicker(7 * 24 * time.Hour)   // Weekly
	monthlyTicker := time.NewTicker(30 * 24 * time.Hour) // Monthly

	go func() {
		for {
			select {
			case <-weeklyTicker.C:
				fmt.Println("Collecting Weekly Utilization Data...")
				collectUtilization("7days")
			case <-monthlyTicker.C:
				fmt.Println("Collecting Monthly Utilization Data...")
				collectUtilization("30days")
			}
		}
	}()
}

func main() {
	initDatabase()
	registerPrometheusMetrics()
	scheduleUtilizationCollection()

	go func() {
		for range time.NewTicker(5 * time.Minute).C {
			updatePrometheusMetrics()
		}
	}()

	http.Handle("/metrics", promhttp.Handler())
	fmt.Println("Serving metrics at /metrics")
	http.ListenAndServe(":9060", nil)
}
