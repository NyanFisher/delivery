package microarch.delivery;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "app")
public class ApplicationProperties {

    private final Grpc grpc = new Grpc();
    private final Kafka kafka = new Kafka();

    public Grpc getGrpc() {
        return grpc;
    }

    public Kafka getKafka() {
        return kafka;
    }

    public static class Grpc {
        private final GeoService geoService = new GeoService();

        public GeoService getGeoService() {
            return geoService;
        }

        public static class GeoService {
            private String host;
            private int port;

            public String getHost() {
                return host;
            }

            public void setHost(String host) {
                this.host = host;
            }

            public int getPort() {
                return port;
            }

            public void setPort(int port) {
                this.port = port;
            }
        }
    }

    public static class Kafka {
        private String stocksEventsTopic;
        private String basketsEventsTopic;

        public String getStocksEventsTopic() {
            return stocksEventsTopic;
        }

        public void setStocksEventsTopic(String stocksEventsTopic) {
            this.stocksEventsTopic = stocksEventsTopic;
        }

        public String getBasketsEventsTopic() {
            return basketsEventsTopic;
        }

        public void setBasketsEventsTopic(String basketsEventsTopic) {
            this.basketsEventsTopic = basketsEventsTopic;
        }
    }
}