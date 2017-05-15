package mapred.allPairs;

/**
 * Created by Darren on 5/6/2017.
 */
public class UserObject {

    private String user;
    private double ascore;

    public UserObject(String user, double ascore) {
        this.user = user;
        this.ascore = ascore;
    }

    public String getUser() {
        return this.user;
    }

    public Double getAscore() {
        return this.ascore;
    }

}
