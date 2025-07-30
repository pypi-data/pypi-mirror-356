#ifdef __cplusplus
extern "C" {
#endif

#define CMD_MAX_INPUT 16
#define CMD_MAX_DIM 8
struct cmdline_options {
    int rest_line_index;
    int input_number;
    struct {
        int dim_count;
        int dims[CMD_MAX_DIM];
    } input_shape[CMD_MAX_INPUT];
    int loop_time;
};

struct cmdline_options *cmdline_parser(int argc, char *argv[]);

#ifdef __cplusplus
}
#endif
